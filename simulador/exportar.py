"""Gera os arquivos estáticos do simulador a partir de data/cebraspe.db.

Saída (fora do git, ver simulador/.gitignore):
  simulador/public/dados/catalogo.json   índice compacto de todas as questões (filtros e sorteio no navegador)
  simulador/public/dados/q/<n>.json      blocos de até TAM_BLOCO questões, com gabarito e textos de apoio
  simulador/public/img/...               só as imagens usadas pelas questões exportadas

Uso:  python simulador/exportar.py [--db data/cebraspe.db] [--limite N]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
SAIDA = AQUI / "public"
TAM_BLOCO = 100
LIMITE_ARQUIVOS = 20_000  # limite de arquivos estáticos por versão no plano gratuito dos Workers
MAX_ARQUIVO = 25 * 1024 * 1024

SQL = """
SELECT q.id, q.tipo, q.numero, q.variante, q.enunciado, q.alternativas_json, q.imagens, q.texto_id,
       q.disciplina, q.assunto, q.bloco,
       c.orgao, c.orgao_nome, c.nome AS concurso, COALESCE(c.ano, p.ano) AS ano, p.cargo,
       g.resposta_preliminar, g.resposta_definitiva, g.anulada, g.alterada, g.justificativa, g.padrao_resposta
FROM questao q
JOIN prova p ON p.id = q.prova_id
JOIN concurso c ON c.id = p.concurso_id
LEFT JOIN gabarito g ON g.questao_id = q.id
ORDER BY q.id
"""


def _json(texto):
    if not texto:
        return None
    try:
        return json.loads(texto)
    except ValueError:
        return None


def _img(caminho: str) -> str | None:
    """'data/img/SLUG/123/x.png' -> 'SLUG/123/x.png' (caminho servido em /img/)."""
    c = caminho.replace("\\", "/")
    for prefixo in ("data/img/", "img/"):
        if c.startswith(prefixo):
            return c[len(prefixo):]
    return None


class Indice:
    """Lista de valores distintos -> posição, para o catálogo guardar números em vez de textos."""

    def __init__(self):
        self.valores: list[str] = []
        self._pos: dict[str, int] = {}

    def __call__(self, v) -> int:
        v = (v or "").strip()
        if v not in self._pos:
            self._pos[v] = len(self.valores)
            self.valores.append(v)
        return self._pos[v]


def exportar(db: Path, limite: int | None = None) -> dict:
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    img_dir = db.parent / "img"

    textos = {r["id"]: r for r in con.execute("SELECT id, rotulo, conteudo, imagens FROM texto_base")}

    dados = SAIDA / "dados"
    if dados.exists():
        shutil.rmtree(dados)
    (dados / "q").mkdir(parents=True)

    disc, org, blo = Indice(), Indice(), Indice()
    cat = {"id": [], "tipo": [], "disc": [], "org": [], "ano": [], "bloco": [], "anul": []}
    imagens: set[str] = set()
    bloco: list[dict] = []
    textos_bloco: dict[int, dict] = {}
    n_bloco = 0
    pulos = {"sem_gabarito": 0}

    def fechar():
        nonlocal bloco, textos_bloco, n_bloco
        if not bloco:
            return
        arq = dados / "q" / f"{n_bloco}.json"
        arq.write_text(json.dumps({"q": bloco, "t": textos_bloco}, ensure_ascii=False, separators=(",", ":")),
                       encoding="utf-8")
        n_bloco += 1
        bloco, textos_bloco = [], {}

    def usar_imgs(lista):
        out = []
        for c in lista or []:
            r = _img(c)
            if r:
                out.append(r)
                imagens.add(r)
        return out

    for r in con.execute(SQL + (f" LIMIT {int(limite)}" if limite else "")):
        tipo = r["tipo"]
        resposta = r["resposta_definitiva"] or r["resposta_preliminar"]
        anulada = bool(r["anulada"]) or resposta == "X"
        if tipo in ("CE", "ME") and not resposta:
            pulos["sem_gabarito"] += 1
            continue

        q = {"id": r["id"], "tp": tipo, "n": r["numero"], "e": r["enunciado"] or ""}
        if r["variante"]:
            q["v"] = r["variante"]
        alts = _json(r["alternativas_json"])
        if alts:
            q["a"] = alts
        ims = usar_imgs(_json(r["imagens"]))
        if ims:
            q["im"] = ims
        for k, col in (("d", "disciplina"), ("as", "assunto"), ("o", "orgao_nome"), ("c", "concurso"),
                       ("ca", "cargo"), ("j", "justificativa"), ("p", "padrao_resposta")):
            if r[col]:
                q[k] = r[col]
        q["an"] = r["ano"]
        if tipo in ("CE", "ME"):
            q["r"] = None if anulada else resposta
            if anulada:
                q["x"] = 1
            if not r["resposta_definitiva"]:
                q["pre"] = 1  # só gabarito preliminar
            if r["alterada"]:
                q["alt"] = r["resposta_preliminar"]

        tid = r["texto_id"]
        if tid and tid in textos:
            q["t"] = tid
            if tid not in textos_bloco:
                t = textos[tid]
                item = {"r": t["rotulo"] or "", "c": t["conteudo"] or ""}
                ti = usar_imgs(_json(t["imagens"]))
                if ti:
                    item["im"] = ti
                textos_bloco[tid] = item

        cat["id"].append(r["id"])
        cat["tipo"].append(tipo)
        cat["disc"].append(disc(r["disciplina"]))
        cat["org"].append(org(r["orgao_nome"] or r["orgao"]))
        cat["ano"].append(r["ano"] or 0)
        cat["bloco"].append(blo(r["bloco"]))
        cat["anul"].append(1 if anulada else 0)

        bloco.append(q)
        if len(bloco) >= TAM_BLOCO:
            fechar()
    fechar()

    catalogo = {"tam_bloco": TAM_BLOCO, "disciplinas": disc.valores, "orgaos": org.valores,
                "blocos": blo.valores, **cat}
    (dados / "catalogo.json").write_text(json.dumps(catalogo, ensure_ascii=False, separators=(",", ":")),
                                         encoding="utf-8")

    # imagens: copia só as usadas e remove as que não são mais usadas
    destino = SAIDA / "img"
    faltando = 0
    for rel in imagens:
        src, dst = img_dir / rel, destino / rel
        if not src.exists():
            faltando += 1
            continue
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    if destino.exists():
        for f in destino.rglob("*"):
            if f.is_file() and f.relative_to(destino).as_posix() not in imagens:
                f.unlink()

    arquivos = [f for f in SAIDA.rglob("*") if f.is_file()]
    grandes = [f for f in arquivos if f.stat().st_size > MAX_ARQUIVO]
    return {"questoes": len(cat["id"]), "blocos": n_bloco, "imagens": len(imagens) - faltando,
            "imagens_faltando": faltando, "arquivos": len(arquivos), "grandes": [str(f) for f in grandes],
            "mb": round(sum(f.stat().st_size for f in arquivos) / 1e6, 1), **pulos}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", type=Path, default=RAIZ / "data" / "cebraspe.db")
    ap.add_argument("--limite", type=int, help="exporta só as N primeiras questões (teste)")
    a = ap.parse_args(argv)
    if not a.db.exists():
        sys.exit(f"Banco não encontrado: {a.db}")
    res = exportar(a.db, a.limite)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if res["arquivos"] > LIMITE_ARQUIVOS:
        sys.exit(f"ERRO: {res['arquivos']} arquivos passam do limite de {LIMITE_ARQUIVOS} do plano gratuito.")
    if res["grandes"]:
        sys.exit("ERRO: arquivos acima de 25 MiB: " + ", ".join(res["grandes"]))


if __name__ == "__main__":
    main()
