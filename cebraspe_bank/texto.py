"""Normalização de texto (acentos, entidades HTML quebradas, espaços)."""
from __future__ import annotations

import html
import re
import unicodedata

_ENT = re.compile(r"&?([A-Za-z])(acute|grave|circ|tilde|cedil|uml);")


def corrigir_entidades(s: str) -> str:
    # "Aacute;REAS" -> "ÁREAS"
    s = _ENT.sub(lambda m: html.unescape(f"&{m.group(1)}{m.group(2)};"), s)
    return html.unescape(s)


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s: str | None) -> str:
    """Maiúsculas, sem acento, travessões/underscores viram espaço, espaços colapsados."""
    if not s:
        return ""
    s = sem_acento(corrigir_entidades(s)).upper()
    s = re.sub(r"[\u2010-\u2015_]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def limpa(s: str | None) -> str:
    return re.sub(r"\s+", " ", corrigir_entidades(s or "")).strip()
