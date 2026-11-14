"""Tabelas de 'Justificativas de alteração/anulação de gabarito'."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .pdf import Documento
from ..texto import norm

_R = r"(?:[A-E]|C|E|CERTO|ERRADO|X)"
_D = r"(?:[‐\-–—]|ANULAD[OA]|NULO)"
_SIT = r"(Deferid\w*.*|Indeferid\w*.*|Anulad\w*.*|Alterad\w*.*|Mantid\w*.*)"
_LINHA = re.compile(rf"^(\d{{1,3}})\s+({_R})\s+({_R}|{_D})\s*{_SIT}?$", re.I)
_LINHA_SO_DEF = re.compile(rf"^(\d{{1,3}})\s+({_R}|{_D})\s*{_SIT}$", re.I)    # tabela sem a coluna preliminar
_CAB = re.compile(r"^(QUEST[ÃA]O|ITEM)\s+GABARITO", re.I)


@dataclass
class LinhaJust:
    secao: str | None
    numero: int
    preliminar: str | None
    definitiva: str             # X = anulada
    situacao: str | None
    texto: str


def _resp(t: str) -> str:
    t = t.upper()
    if t in ("CERTO",):
        return "C"
    if t in ("ERRADO",):
        return "E"
    if t in ("‐", "-", "–", "—", "ANULADO", "ANULADA", "NULO", "X"):
        return "X"
    return t


def _eh_titulo(t: str) -> bool:
    return bool(t) and len(t) < 200 and not re.match(r"^\d", t) and (
        t.upper() == t or re.match(r"^(PROVA|CARGO|CONHECIMENTOS|BLOCO|[ÁA]REA|ESPECIALIDADE|C\d{2}\b)", norm(t)))


def atual_texto_continua(atual, texto: list[str], t: str) -> bool:
    """Linha em maiúsculas que é continuação do texto da justificativa (ex.: siglas longas) não abre seção."""
    return bool(atual and texto and not texto[-1].rstrip().endswith((".", ":", ")")) and len(t.split()) > 12)


def parse(doc: Documento) -> list[LinhaJust]:
    out: list[LinhaJust] = []
    secao_partes: list[str] = []
    atual: LinhaJust | None = None
    texto: list[str] = []

    def fecha():
        nonlocal atual
        if atual:
            atual.texto = " ".join(texto).strip()
            out.append(atual)
        atual = None
        texto.clear()

    linhas = doc.linhas
    cab = [k for k, l in enumerate(linhas) if _CAB.match(l.texto.strip())]
    titulos: set[int] = set()
    for k in cab:            # títulos de seção = linhas em maiúsculas imediatamente antes do cabeçalho da tabela
        j = k - 1
        while j >= 0 and j not in titulos and _eh_titulo(linhas[j].texto.strip()) and \
                not (_LINHA.match(linhas[j].texto.strip()) or _LINHA_SO_DEF.match(linhas[j].texto.strip())):
            titulos.add(j)
            j -= 1
    for idx, l in enumerate(linhas):
        t = l.texto.strip()
        if _CAB.match(t):
            fecha()
            continue
        m = _LINHA.match(t)
        m1 = None if m else _LINHA_SO_DEF.match(t)
        if m or m1:
            fecha()
            if m:
                pre, de, sit = _resp(m.group(2)), _resp(m.group(3)), (m.group(4) or "").strip() or None
            else:
                pre, de, sit = None, _resp(m1.group(2)), m1.group(3).strip()
            if sit and re.search(r"anula", sit, re.I):
                de = "X"
            atual = LinhaJust(" / ".join(secao_partes) or None, int((m or m1).group(1)), pre, de, sit, "")
            continue
        tn = norm(t)
        if idx in titulos and idx - 1 in titulos and secao_partes and \
                not re.match(r"^(PROVA|CONHECIMENTOS|BLOCO|CARGO|C\d{2}\b)", tn):
            secao_partes[-1] = f"{secao_partes[-1]} {t}"      # título quebrado em duas linhas
            continue
        if idx in titulos:
            fecha()
            if re.match(r"^(PROVA|CONHECIMENTOS|BLOCO|PARTE|M[OÓ]DULO)", tn):
                if re.match(r"^(PROVA|CONHECIMENTOS)", tn) and secao_partes and re.match(r"^BLOCO", norm(secao_partes[-1])):
                    secao_partes.append(t)
                else:
                    secao_partes = [t]
            else:
                secao_partes = [p for p in secao_partes if re.match(r"^(PROVA|CONHECIMENTOS|BLOCO)", norm(p))]
                secao_partes.append(t)
            continue
        if atual:
            texto.append(t)
    fecha()
    return out
