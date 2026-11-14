"""Formatos em que prova e gabarito vêm no mesmo PDF.

1. 2025+: "1 B0703445 - CORRETO | enunciado" (cada item com código, resposta e comando próprio).
2. 2022–2024: prova de múltipla escolha/CE seguida de "||JUSTIFICATIVAS||" com "||A|| - Correta. ...".
"""
from __future__ import annotations

import re

from .pdf import Documento, Linha
from .prova import Bloco, Item, ResultadoProva, _JUST_ALT, junta, segmentar

_ITEM_COD = re.compile(
    r"^(\d{1,3})\s+([A-Z]{1,2}\d{5,9})\s*[-–]\s*(CORRETO|ERRADO|CERTO|ANULAD[OA]|[A-E]|X)"
    r"(\s*[-–]\s*ANULAD[OA])?\s*\|\s*(.*)$", re.I)
_ITEM_SEM_COD = re.compile(r"^(\d{1,3})\s+(CORRETO|ERRADO|CERTO)(\s*[-–]\s*ANULAD[OA])?\s*\|\s*(.*)$", re.I)
_RESP = {"CORRETO": "C", "CERTO": "C", "ERRADO": "E", "ANULADO": "X", "ANULADA": "X"}


def _casa_item(t: str):
    """Normaliza as duas variantes para (numero, codigo, resposta, anulado, texto)."""
    m = _ITEM_COD.match(t)
    if m:
        return m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    m = _ITEM_SEM_COD.match(t)
    if m:
        return m.group(1), None, m.group(2), m.group(3), m.group(4)
    return None


def eh_formato_codigo(doc: Documento) -> bool:
    return sum(1 for l in doc.linhas[:200] if _casa_item(l.texto)) >= 2


def segmentar_codigo(doc: Documento) -> tuple[ResultadoProva, dict[int, str]]:
    itens: list[Item] = []
    blocos: list[Bloco] = []
    respostas: dict[int, str] = {}
    atual: Item | None = None
    bloco: Bloco | None = None
    recentes: list[Bloco] = []
    secao = None
    for l in doc.linhas:
        m = _casa_item(l.texto)
        if m:
            num, cod, resp, anul, txt = m
            n = int(num)
            orig = _RESP.get(resp.upper(), resp.upper())
            r = "X" if anul else orig
            atual = Item(n, "CE" if orig in ("C", "E") else "ME", secao=secao, numero_bruto=num)
            atual.codigo_item = cod
            atual.linhas.append(Linha(l.pagina, l.col, l.x0, l.y0, l.x1, l.y1, txt, l.tamanho, l.origem))
            atual.blocos_anteriores = list(recentes)
            atual.bloco = recentes[-1] if recentes else None
            itens.append(atual)
            respostas[n] = r
            bloco = None
            recentes = []
            continue
        sm = re.match(r"^-{2,}\s*(.+?)\s*-{2,}$", l.texto)
        if sm:
            secao = sm.group(1)
            atual = None
            continue
        if atual is not None and l.x0 > atual.linhas[0].x0 + 8 and l.pagina == atual.linhas[-1].pagina:
            atual.linhas.append(l)
            continue
        if atual is not None and l.pagina != atual.linhas[-1].pagina and l.x0 > 40:
            atual.linhas.append(l)
            continue
        atual = None
        if bloco is None:
            bloco = Bloco(len(blocos) + 1, [l])
            blocos.append(bloco)
            recentes.append(bloco)
        else:
            bloco.linhas.append(l)
    # cabeçalho de cargo/bloco antes do 1º comando não é texto-base
    tipos = {i.tipo for i in itens}
    tipo = tipos.pop() if len(tipos) == 1 else "misto"
    return ResultadoProva(itens, blocos, tipo, None, []), respostas


def respostas_de_justificativas(res: ResultadoProva) -> dict[int, str]:
    """Para provas 'com justificativas': a alternativa marcada como 'Correta' (ME) ou CERTO/ERRADO (CE)."""
    out: dict[int, str] = {}
    for it in res.itens:
        if not it.justificativa:
            continue
        texto = junta(it.justificativa)
        if it.tipo == "ME":
            corretas = [m.group(1) for l in it.justificativa for m in [_JUST_ALT.match(l.texto)]
                        if m and re.match(r"^-?\s*Corret", m.group(2), re.I)]
            if len(corretas) == 1:
                out[it.numero] = corretas[0]
            elif len(corretas) > 1:
                out[it.numero] = "X"
        else:
            m = re.match(r"^\s*\|*\s*JUSTIFICATIVAS?\|*\s*[-–:]?\s*(CERTO|ERRADO|CORRETO|INCORRETO|ANULAD)", texto.upper()) \
                or re.search(r"\b(CERTO|ERRADO|CORRETO|INCORRETO)\b", texto.upper())
            if m:
                out[it.numero] = "X" if m.group(1) == "ANULAD" else ("C" if m.group(1) in ("CERTO", "CORRETO") else "E")
    return out


def segmentar_auto(doc: Documento, modalidade: str | None, esperados: set[int] | None
                   ) -> tuple[ResultadoProva, dict[int, str], str]:
    """Escolhe o formato. Retorna (resultado, respostas embutidas, formato)."""
    if eh_formato_codigo(doc):
        r, resp = segmentar_codigo(doc)
        return r, resp, "codigo"
    r = segmentar(doc, modalidade, esperados)
    resp = respostas_de_justificativas(r)
    return r, resp, ("com_justificativas" if resp else "padrao")
