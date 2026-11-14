"""Regras de ano do concurso.

Precedência (ano = ano do edital de abertura):
  1. edital_pdf         — "EDITAL Nº 1 – X, DE dd DE mês DE aaaa" lido de prova/gabarito/edital (Fases 3/4)
  2. edital_nome        — ano no nome do arquivo do Edital nº 1 de abertura (ex.: ED_1_2023_CAPES_ABERTURA.PDF)
  3. edital_publicacao  — data de publicação do Edital nº 1 de abertura no site
  4. slug               — ano no slug/nome do concurso (CAPES_23, INSS_2015)
  5. aplicacao          — data de aplicação da prova
eventoAno da API fica em ano_api, só como evidência.
"""
from __future__ import annotations

import re

PRECEDENCIA = ["edital_pdf", "edital_nome", "edital_publicacao", "slug", "aplicacao"]
FONTES_EDITAL = {"edital_pdf", "edital_nome", "edital_publicacao"}

MESES = {m: i + 1 for i, m in enumerate(
    ["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO",
     "NOVEMBRO", "DEZEMBRO"])}


def _ano_valido(a: int | None) -> int | None:
    return a if a and 1990 <= a <= 2100 else None


def slug_tokens(slug: str) -> tuple[str | None, int | None]:
    """Retorna (orgao, ano_slug). orgao = tokens antes do token de ano."""
    toks = slug.split("_")
    for i, t in enumerate(toks):
        if i == 0:
            continue
        if re.fullmatch(r"(19|20)\d{2}", t):
            return "_".join(toks[:i]) or None, _ano_valido(int(t))
        if re.fullmatch(r"\d{2}", t) and 10 <= int(t) <= 49:
            return "_".join(toks[:i]) or None, 2000 + int(t)
    m = re.search(r"(?<!\d)(20\d{2})(?!\d)", slug)
    if m:
        return slug[: m.start()].rstrip("_") or None, int(m.group(1))
    return slug, None


def ano_nome_edital(nome_arquivo: str) -> int | None:
    m = re.search(r"(?i)\bED(?:ITAL)?[_ .]*N?[_ .]*0*1[_ .]+((?:19|20)\d{2})[_ .]", nome_arquivo + "_")
    return _ano_valido(int(m.group(1))) if m else None


_DATA_EDITAL = re.compile(
    r"EDITAL\s+N(?:O|\.|°|º)?\W{0,3}\s*0*1\b[^\n]{0,80}?,?\s+DE\s+(\d{1,2})(?:º|O)?\s+DE\s+([A-Z]+)\s+DE\s+((?:19|20)\d{2})"
)
_APLIC = re.compile(r"APLICA[CÇ][AÃ]O:\s*(\d{1,2})/(\d{1,2})/((?:19|20)\d{2}|\d{2})\b", re.I)
_APLIC_ANO = re.compile(r"APLICA[CÇ][AÃ]O:\s*((?:19|20)\d{2})\b", re.I)


def data_edital_texto(texto_norm: str) -> str | None:
    """texto_norm: texto já normalizado (maiúsculas, sem acento). Retorna data ISO do Edital nº 1."""
    m = _DATA_EDITAL.search(texto_norm)
    if not m:
        return None
    dia, mes, ano = int(m.group(1)), MESES.get(m.group(2)), int(m.group(3))
    if not mes or not 1 <= dia <= 31:
        return None
    return f"{ano:04d}-{mes:02d}-{dia:02d}"


def data_aplicacao_texto(texto: str) -> str | None:
    m = _APLIC.search(texto)
    if m:
        d, mth, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = a + 2000 if a < 100 else a
        if 1 <= d <= 31 and 1 <= mth <= 12:
            return f"{a:04d}-{mth:02d}-{d:02d}"
    return None


def ano_aplicacao_texto(texto: str) -> int | None:
    iso = data_aplicacao_texto(texto)
    if iso:
        return int(iso[:4])
    m = _APLIC_ANO.search(texto)
    return int(m.group(1)) if m else None


def resolver(candidatos: dict[str, int | None]) -> tuple[int | None, str | None]:
    for f in PRECEDENCIA:
        v = _ano_valido(candidatos.get(f))
        if v:
            return v, f
    return None, None
