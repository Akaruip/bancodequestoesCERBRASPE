"""CLI: python -m cebraspe_bank {crawl,download,extract,classify,validate,report} [--concurso SLUG] [--ano ANO] [--desde ANO]"""
from __future__ import annotations

import argparse
import json
import logging
import sys

from . import config, db


def _filtros(p: argparse.ArgumentParser) -> None:
    p.add_argument("--concurso", action="append", metavar="SLUG", help="slug do concurso (pode repetir)")
    p.add_argument("--ano", type=int, help="só concursos deste ano")
    p.add_argument("--desde", type=int, help="só concursos a partir deste ano")
    p.add_argument("--db", default=str(config.DB_PATH), help="caminho do banco SQLite")
    p.add_argument("-v", "--verbose", action="store_true")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="cebraspe_bank", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("crawl", help="Fase 1: metadados de concursos e documentos")
    _filtros(p)
    p.add_argument("--refresh", action="store_true", help="reconsulta também concursos encerrados já coletados")

    p = sub.add_parser("download", help="Fase 2: baixa provas, gabaritos, justificativas e padrões")
    _filtros(p)
    p.add_argument("--limite", type=int, help="máximo de arquivos nesta execução")
    p.add_argument("--editais", action="store_true",
                   help="baixa também o edital de abertura dos concursos sem ano confirmado por edital")
    p.add_argument("--editais-conteudo", action="store_true",
                   help="baixa SÓ o edital de abertura (PDF) de todo concurso com provas, para a classificação por "
                        "disciplina pelo conteúdo programático (Fase 5b)")

    p = sub.add_parser("extract", help="Fases 3-4: extrai questões e gabaritos dos PDFs")
    _filtros(p)
    p.add_argument("--refazer", action="store_true", help="reprocessa documentos já extraídos")
    p.add_argument("--revincular", action="store_true",
                   help="refaz só o vínculo prova↔gabarito/justificativas/padrões de todos os concursos selecionados")

    p = sub.add_parser("classify", help="Fase 5: bloco, assunto e disciplina das questões (regras, sem LLM)")
    _filtros(p)

    p = sub.add_parser("validate", help="valida a consistência e gera a amostra de revisão")
    _filtros(p)
    p.add_argument("--amostra", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)

    p = sub.add_parser("report", help="gera REPORT_FINAL.md")
    _filtros(p)
    p.add_argument("--saida", default=str(config.ROOT / "REPORT_FINAL.md"))

    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s", stream=sys.stderr)
    con = db.conectar(a.db)
    filtros = dict(slugs=a.concurso, ano=a.ano, desde=a.desde)

    if a.cmd == "crawl":
        from .crawl import crawl
        from .rede import Cliente
        res = crawl(con, Cliente(), refresh=a.refresh, **filtros)
    elif a.cmd == "download":
        from .download import download
        from .rede import Cliente
        res = download(con, Cliente(), limite=a.limite, editais=a.editais, conteudo=a.editais_conteudo, **filtros)
    elif a.cmd == "extract":
        from .extract import extract
        res = extract(con, refazer=a.refazer, revincular=a.revincular, **filtros)
    elif a.cmd == "classify":
        from .disciplina import classificar
        res = classificar(con, **filtros)
    elif a.cmd == "validate":
        from .validate import validate
        res = validate(con, amostra=a.amostra, seed=a.seed, **filtros)
    else:
        from .report import report
        res = report(con, saida=a.saida, **filtros)
    print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    return 0
