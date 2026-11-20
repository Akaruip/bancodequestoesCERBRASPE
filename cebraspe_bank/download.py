"""Fase 2 — download idempotente dos PDFs para data/raw/{ano}/{slug}/{nome_original}."""
from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path

from . import config, db
from .rede import Cliente

log = logging.getLogger(__name__)

TIPOS_DOWNLOAD = ("prova", "prova_com_gabarito_preliminar", "prova_com_gabarito_definitivo",
                  "gabarito_preliminar", "gabarito_definitivo", "justificativa", "padrao_resposta")
# o edital de abertura só é baixado se o ano ainda não veio de uma fonte de edital
FONTES_SEM_EDITAL = ("slug", "aplicacao")


def sha256_arquivo(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def caminho_local(ano: int | None, slug: str, nome: str) -> Path:
    nome = nome.replace("/", "_").replace("\\", "_").strip()
    return config.RAW_DIR / (str(ano) if ano else "sem_ano") / slug / nome


def _selecao(con, slugs, ano, desde, editais: bool, conteudo: bool = False):
    # conteudo=True: também o edital de abertura em PDF de todo concurso com provas (conteúdo programático usado na
    # classificação por disciplina, Fase 5b) — um por concurso: o "atualizado conforme retificações", se houver
    q = f"""SELECT d.*, c.slug, c.ano AS c_ano, c.ano_fonte FROM documento d JOIN concurso c ON c.id=d.concurso_id
            WHERE d.acessibilidade=0 AND d.removido_do_site=0 AND COALESCE(d.versao,'')<>'sem_efeito'
            AND (d.tipo IN ({','.join('?' * len(TIPOS_DOWNLOAD))})
                 OR (d.tipo='edital_abertura' AND (c.ano_fonte IS NULL OR c.ano_fonte IN ('slug','aplicacao')
                                                   OR (? AND c.ano_fonte='edital_publicacao')))
                 OR (? AND d.tipo='edital_abertura' AND lower(COALESCE(d.extensao,''))='pdf'
                     AND EXISTS (SELECT 1 FROM prova p WHERE p.concurso_id=c.id)
                     AND (COALESCE(d.versao,'')='atualizado' OR NOT EXISTS (
                          SELECT 1 FROM documento d2 WHERE d2.concurso_id=d.concurso_id AND d2.tipo='edital_abertura'
                          AND d2.acessibilidade=0 AND d2.removido_do_site=0 AND d2.versao='atualizado'
                          AND lower(COALESCE(d2.extensao,''))='pdf'))))"""
    args: list = [*TIPOS_DOWNLOAD, int(editais), int(conteudo)]
    if slugs:
        q += f" AND c.slug IN ({','.join('?' * len(slugs))})"
        args += slugs
    if ano:
        q += " AND c.ano=?"
        args.append(ano)
    if desde:
        q += " AND c.ano>=?"
        args.append(desde)
    return con.execute(q + " ORDER BY c.ano DESC, c.slug, d.id", args).fetchall()


def download(con, cli: Cliente, slugs=None, ano=None, desde=None, limite: int | None = None,
             editais: bool = False, conteudo: bool = False) -> dict:
    docs = _selecao(con, slugs, ano, desde, editais, conteudo)
    if conteudo:        # --editais-conteudo baixa só os editais de abertura (não mexe nas provas/gabaritos)
        docs = [d for d in docs if d["tipo"] == "edital_abertura"]
    st = {"selecionados": len(docs), "ja_existiam": 0, "registrados_sem_baixar": 0, "baixados": 0,
          "falhas": 0, "bytes": 0}
    for d in docs:
        destino = Path(d["arquivo_local"]) if d["arquivo_local"] else caminho_local(d["c_ano"], d["slug"], d["nome_arquivo"])
        if not destino.is_absolute():
            destino = config.ROOT / destino
        if destino.exists():
            h = sha256_arquivo(destino)
            if d["sha256"] == h:
                st["ja_existiam"] += 1
                continue
            if d["sha256"] is None:  # arquivo presente mas não registrado: registra sem baixar de novo
                _registra(con, d["id"], destino, h, 200)
                st["registrados_sem_baixar"] += 1
                continue
            log.warning("hash divergente em %s: rebaixando", destino)
        if "\ufffd" in d["nome_arquivo"]:
            _falha(con, d, "nome do arquivo corrompido na API (caractere inválido); URL irrecuperável")
            st["falhas"] += 1
            continue
        if limite is not None and st["baixados"] + st["falhas"] >= limite:
            st["adiados"] = st.get("adiados", 0) + 1
            continue
        try:
            r = cli.get(d["url"])
        except Exception as e:  # noqa: BLE001
            _falha(con, d, f"erro de rede: {type(e).__name__}: {e}")
            st["falhas"] += 1
            continue
        if r.status != 200 or not r.content:
            _falha(con, d, f"HTTP {r.status}", r.status)
            st["falhas"] += 1
            continue
        ext = (d["extensao"] or "").lower()
        if ext in ("pdf", "") and not r.content.lstrip()[:5].startswith(b"%PDF"):
            _falha(con, d, f"conteúdo não é PDF (Content-Type {r.content_type})", r.status)
            st["falhas"] += 1
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        tmp = destino.with_name(destino.name + ".part")
        tmp.write_bytes(r.content)
        os.replace(tmp, destino)
        _registra(con, d["id"], destino, hashlib.sha256(r.content).hexdigest(), r.status)
        db.resolver_pendencias(con, "download", d["concurso_id"], d["id"])
        con.commit()
        st["baixados"] += 1
        st["bytes"] += len(r.content)
        if st["baixados"] % 50 == 0:
            log.info("baixados %d (%.1f MB)", st["baixados"], st["bytes"] / 1e6)
    con.commit()
    return st


def _registra(con, doc_id: int, destino: Path, sha: str, status: int) -> None:
    try:
        rel = destino.relative_to(config.ROOT)
    except ValueError:
        rel = destino
    con.execute("UPDATE documento SET arquivo_local=?, sha256=?, tamanho=?, http_status=?, baixado_em=? WHERE id=?",
                (str(rel), sha, destino.stat().st_size, status, db.agora(), doc_id))
    con.commit()


def _falha(con, d, motivo: str, status: int | None = None) -> None:
    con.execute("UPDATE documento SET http_status=? WHERE id=?", (status, d["id"]))
    db.pendencia(con, "download", motivo, d["concurso_id"], d["id"])
    con.commit()
    log.warning("%s %s: %s", d["slug"], d["nome_arquivo"], motivo)
