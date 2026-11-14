"""Fase 1 — crawler de metadados (concursos e documentos) via API JSON do Cebraspe."""
from __future__ import annotations

import hashlib
import json
import logging
from urllib.parse import quote

from . import anos, config, db
from .classify import classificar
from .rede import Cliente
from .texto import limpa

log = logging.getLogger(__name__)

STATUS_FASE = {"Novos": "novos", "Inscrições Abertas": "inscricoes-abertas",
               "Em Andamento": "em-andamento", "Encerrados": "encerrado"}


def url_arquivo(slug: str, item: dict) -> str:
    nome = item["nomeArquivo"]
    if item.get("isGuid"):
        return config.CDN_BASE + quote(nome)
    if item.get("tipoExtensaoArquivo") == "_explorer":
        return f"http://www.cespe.unb.br/concursos/{slug}/arquivos/{quote(nome)}"
    return f"{config.CDN_BASE}concursos/{slug}/arquivos/{quote(nome)}"


def _salva_json(sub: str, nome: str, conteudo: bytes) -> str:
    d = config.API_DIR / sub
    d.mkdir(parents=True, exist_ok=True)
    (d / nome).write_bytes(conteudo)
    return hashlib.sha256(conteudo).hexdigest()


def atualizar_lista(con, cli: Cliente) -> list[dict]:
    r = cli.get(config.LISTA_CONCURSOS)
    if r.status != 200:
        raise RuntimeError(f"listagem de concursos falhou: HTTP {r.status}")
    _salva_json("", "lista_concursos.json", r.content)
    grupos = json.loads(r.content)
    vistos: dict[str, dict] = {}
    for g in grupos:
        for e in g.get("eventos") or []:
            slug = e["eventoURL"].strip()
            e["_status"] = e.get("eventoStatus") or STATUS_FASE.get(g.get("faseEvento"))
            vistos.setdefault(slug, e)  # slug duplicado (ex.: INSS_22) => primeira ocorrência
    for slug, e in vistos.items():
        orgao, ano_slug = anos.slug_tokens(slug)
        con.execute(
            """INSERT INTO concurso(slug, orgao, nome, ano_slug, ano_api, url, status, atualizado_em)
               VALUES (?,?,?,?,?,?,?,?)
               ON CONFLICT(slug) DO UPDATE SET nome=excluded.nome, ano_slug=excluded.ano_slug,
                 ano_api=excluded.ano_api, status=excluded.status, orgao=COALESCE(concurso.orgao, excluded.orgao),
                 url=excluded.url, atualizado_em=excluded.atualizado_em""",
            (slug, orgao, limpa(e.get("eventoNomeAbreviado")), ano_slug, e.get("eventoAno"),
             config.SITE_CONCURSO.format(slug=slug), e["_status"], db.agora()),
        )
    con.commit()
    log.info("listagem: %d concursos", len(vistos))
    return list(vistos.values())


def _upsert_documentos(con, concurso_id: int, slug: str, det: dict) -> tuple[int, int]:
    agora = db.agora()
    urls_atuais = set()
    novos = 0
    for lista, chave in (("edital", "arquivosEdital"), ("gabarito", "arquivosGabarito")):
        for it in det.get(chave) or []:
            nome = (it.get("nomeArquivo") or "").strip()
            if not nome:
                continue
            url = url_arquivo(slug, it)
            if url in urls_atuais:
                continue
            urls_atuais.add(url)
            c = classificar(nome, it.get("descricaoArquivo"), it.get("tipoExtensaoArquivo"))
            data_pub = it.get("dataArquivoObj") if it.get("isDataValid") else None
            ext = (it.get("tipoExtensaoArquivo") or "").lower().lstrip("_.") or None
            cur = con.execute("SELECT id, tipo, revisar FROM documento WHERE url=?", (url,)).fetchone()
            vals = dict(concurso_id=concurso_id, tipo=c.tipo, modalidade=c.modalidade, revisar=int(c.revisar),
                        motivo_revisao="; ".join(c.motivos) or None, acessibilidade=int(c.acessibilidade),
                        versao=c.versao, cargo=c.cargo, caderno=c.caderno, codigo_prova=c.codigo_prova,
                        bloco=c.bloco, descricao=limpa(it.get("descricaoArquivo")), nome_arquivo=nome,
                        extensao=ext, lista_origem=lista, data_publicacao=data_pub, url=url, visto_em=agora)
            if cur is None:
                cols = ",".join(vals)
                con.execute(f"INSERT INTO documento({cols}) VALUES ({','.join('?' * len(vals))})", tuple(vals.values()))
                novos += 1
                doc_id = con.execute("SELECT id FROM documento WHERE url=?", (url,)).fetchone()[0]
            else:
                doc_id = cur["id"]
                # tipo revisado manualmente (revisar=0 e tipo diferente do automático) não é sobrescrito
                sets = ",".join(f"{k}=?" for k in vals) + ",removido_do_site=0"
                con.execute(f"UPDATE documento SET {sets} WHERE id=?", (*vals.values(), doc_id))
            if c.revisar:
                db.pendencia(con, "classificacao", "; ".join(c.motivos), concurso_id, doc_id)
    # documentos que sumiram do site: marca, não apaga
    for row in con.execute("SELECT id, url FROM documento WHERE concurso_id=? AND removido_do_site=0", (concurso_id,)):
        if row["url"] not in urls_atuais:
            con.execute("UPDATE documento SET removido_do_site=1 WHERE id=?", (row["id"],))
    return len(urls_atuais), novos


def recalcular_ano(con, concurso_id: int) -> None:
    """Aplica a precedência de ano com o que já se sabe (inclui ano_edital/ano_aplicacao vindos dos PDFs)."""
    c = con.execute("SELECT * FROM concurso WHERE id=?", (concurso_id,)).fetchone()
    cand: dict[str, int | None] = {"slug": c["ano_slug"], "aplicacao": c["ano_aplicacao"]}
    if c["data_edital_pdf"]:
        cand["edital_pdf"] = int(c["data_edital_pdf"][:4])
    # edital de abertura listado no site
    ab_nome, ab_pub = [], []
    for d in con.execute(
        "SELECT nome_arquivo, data_publicacao FROM documento WHERE concurso_id=? AND tipo='edital_abertura' "
        "AND removido_do_site=0", (concurso_id,)):
        a = anos.ano_nome_edital(d["nome_arquivo"])
        if a:
            ab_nome.append(a)
        if d["data_publicacao"]:
            ab_pub.append(d["data_publicacao"][:10])
    if ab_nome:
        cand["edital_nome"] = min(ab_nome)
    if ab_pub:
        cand["edital_publicacao"] = int(min(ab_pub)[:4])
    ano, fonte = anos.resolver(cand)
    ano_edital = next((cand[f] for f in anos.PRECEDENCIA if f in anos.FONTES_EDITAL and cand.get(f)), None)
    data_edital = (c["data_edital_pdf"] if fonte == "edital_pdf"
                   else min(ab_pub) if fonte == "edital_publicacao" else None)
    con.execute("UPDATE concurso SET ano=?, ano_fonte=?, ano_edital=?, data_edital=? WHERE id=?",
                (ano, fonte, ano_edital, data_edital, concurso_id))
    if ano is None:
        db.pendencia(con, "ano", "nenhuma fonte de ano (edital, slug, aplicação)", concurso_id)
    else:
        db.resolver_pendencias(con, "ano", concurso_id)
    # fontes divergentes ficam registradas
    vals = {k: v for k, v in cand.items() if v}
    if len(set(vals.values())) > 1:
        db.checkpoint(con, "ano_divergente", c["slug"], "info", json.dumps(vals, ensure_ascii=False))


def crawl(con, cli: Cliente, slugs: list[str] | None = None, ano: int | None = None, desde: int | None = None,
          refresh: bool = False) -> dict:
    atualizar_lista(con, cli)
    q = "SELECT * FROM concurso WHERE 1=1"
    args: list = []
    if slugs:
        q += f" AND slug IN ({','.join('?' * len(slugs))})"
        args += slugs
    anoexpr = "COALESCE(ano, ano_slug, ano_api)"
    if ano:
        q += f" AND {anoexpr}=?"
        args.append(ano)
    if desde:
        q += f" AND {anoexpr}>=?"
        args.append(desde)
    alvo = con.execute(q + " ORDER BY slug", args).fetchall()
    stats = {"alvo": len(alvo), "consultados": 0, "ok": 0, "falhas": 0, "docs_novos": 0, "pulados": 0}
    for c in alvo:
        precisa = refresh or not c["detalhe_ok"] or c["status"] != "encerrado"
        ck = con.execute("SELECT status FROM checkpoint WHERE etapa='crawl' AND chave=?", (c["slug"],)).fetchone()
        if ck and ck["status"] == "ok_encerrado" and not refresh:
            precisa = False
        if not precisa:
            stats["pulados"] += 1
            continue
        if c["slug"].upper().startswith("TESTE"):
            db.pendencia(con, "crawl", "concurso de teste publicado na API; ignorado", c["id"])
            con.commit()
            stats["pulados"] += 1
            continue
        stats["consultados"] += 1
        r = cli.get(config.DETALHE_EVENTO.format(slug=quote(c["slug"])))
        det = None
        if r.status == 200 and r.content:
            try:
                det = json.loads(r.content)
            except json.JSONDecodeError:
                det = None
        if not det or "arquivosGabarito" not in det:
            stats["falhas"] += 1
            motivo = f"API detalhe HTTP {r.status}" + ("" if r.content else " (corpo vazio)")
            if r.content:
                _salva_json("eventos_erro", f"{c['slug']}.json", r.content)
            con.execute("UPDATE concurso SET detalhe_ok=0, detalhe_http=?, atualizado_em=? WHERE id=?",
                        (r.status, db.agora(), c["id"]))
            db.pendencia(con, "crawl", motivo, c["id"])
            db.checkpoint(con, "crawl", c["slug"], "falha", motivo)
            recalcular_ano(con, c["id"])
            con.commit()
            log.warning("%s: %s", c["slug"], motivo)
            continue
        sha = _salva_json("eventos", f"{c['slug']}.json", r.content)
        status = (det.get("eventoStatus") or c["status"] or "").strip().lower().replace(" ", "-")
        status = {"encerrado": "encerrado"}.get(status, c["status"])  # status da listagem é a referência
        con.execute(
            """UPDATE concurso SET id_evento=?, periodo_inscricao=?, detalhe_ok=1, detalhe_http=200, json_sha256=?,
               atualizado_em=? WHERE id=?""",
            (det.get("idEvento"), limpa(det.get("periodoInscricao")) or None, sha, db.agora(), c["id"]))
        n, novos = _upsert_documentos(con, c["id"], c["slug"], det)
        stats["docs_novos"] += novos
        db.resolver_pendencias(con, "crawl", c["id"])
        recalcular_ano(con, c["id"])
        db.checkpoint(con, "crawl", c["slug"], "ok_encerrado" if status == "encerrado" else "ok", f"{n} docs")
        con.commit()
        stats["ok"] += 1
        log.info("%s: %d documentos (%d novos)", c["slug"], n, novos)
    return stats
