"""Parse dos gabaritos oficiais (grade Item/Gabarito) por coordenadas, com OCR de fallback."""
from __future__ import annotations

import logging
import re
import statistics
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from .. import anos
from ..texto import norm

log = logging.getLogger(__name__)

RESPOSTAS = {"C", "E", "A", "B", "D", "X"}
_VAZIO = {"0", "-", "—", "–", "*"}
_COD = re.compile(r"\b(\d{3}_?[A-Z0-9]+(?:_[A-Z0-9]+)*?_\d{2,3})\b")


@dataclass
class GabaritoPagina:
    pagina: int
    respostas: dict[int, str] = field(default_factory=dict)
    variantes: dict[str, dict[int, str]] = field(default_factory=dict)   # ex.: {"LÍNGUA INGLESA": {1: "C", ...}}
    codigo_prova: str | None = None
    caderno: str | None = None
    cargo: str | None = None
    fase: str | None = None              # preliminar | definitivo
    data_edital: str | None = None
    data_aplicacao: str | None = None
    texto_cabecalho: str = ""
    origem: str = "pdf"
    avisos: list[str] = field(default_factory=list)


def _palavras(page) -> tuple[list, str]:
    w = page.get_text("words")
    if sum(len(x[4]) for x in w) >= 20:
        return w, "pdf"
    try:
        tp = page.get_textpage_ocr(language="por", dpi=300, full=True)
        return page.get_text("words", textpage=tp), "ocr"
    except Exception as e:  # noqa: BLE001
        log.warning("OCR falhou: %s", e)
        return w, "pdf"


def _linhas(words, tol=2.5):
    ws = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    out: list[list] = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if out and abs(out[-1][0] - yc) <= tol:
            out[-1][1].append(w)
        else:
            out.append([yc, [w]])
    return [(yc, sorted(lw, key=lambda w: w[0])) for yc, lw in out]


def _linha_numeros(lw) -> list | None:
    nums = [w for w in lw if re.fullmatch(r"\d{1,3}", w[4]) and int(w[4]) > 0]
    outros = [w for w in lw if w[4] not in _VAZIO]
    if len(nums) < 2 or len(nums) < 0.7 * len(outros):
        return None
    vals = [int(w[4]) for w in nums]
    crescente = sum(1 for a, b in zip(vals, vals[1:]) if b == a + 1)
    if crescente < 0.7 * (len(vals) - 1):
        return None
    return nums


def _eh_resposta(tok: str) -> bool:
    return tok.upper() in RESPOSTAS or tok in _VAZIO


_LINGUA = re.compile(r"L[ÍI]NGUA\s+(INGLESA|ESPANHOLA|FRANCESA|ALEM[ÃA]|ITALIANA|PORTUGUESA)", re.I)


def _cor(c) -> tuple | None:
    if not c:
        return None
    c = tuple(round(float(v), 2) for v in c[:3])
    return None if all(v >= 0.95 for v in c) else c


def _mesma_cor(a, b, tol=0.06) -> bool:
    return a is not None and b is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def _preenchimentos(page) -> list[tuple]:
    out = []
    for d in page.get_drawings():
        c = _cor(d.get("fill"))
        r = d.get("rect")
        if c and r is not None and r.width < page.rect.width * 0.95 and r.height < page.rect.height * 0.5:
            out.append((r, c))
    return out


def _legenda(linhas, fills) -> dict[tuple, str]:
    """cor -> rótulo (ex.: 'LÍNGUA INGLESA'), a partir das amostras de cor ao lado do texto da legenda."""
    leg: dict[tuple, str] = {}
    for _, lw in linhas:
        texto = " ".join(w[4] for w in lw)
        m = _LINGUA.search(texto)
        if not m:
            continue
        ini = next((w for w in lw if _LINGUA.match(w[4] + " " + "X") or w[4].upper().startswith(("LÍNGUA", "LINGUA"))), lw[0])
        yc = (ini[1] + ini[3]) / 2
        cand = [(r, c) for r, c in fills if r.y0 - 2 <= yc <= r.y1 + 2 and r.x1 <= ini[0] + 4 and r.x1 >= ini[0] - 60
                and r.width < 80]
        if cand:
            r, c = max(cand, key=lambda rc: rc[0].x1)
            leg[c] = norm(m.group(0)).replace("LINGUA", "LÍNGUA")
    return leg


def _rotulo(cor, legenda: dict[tuple, str]) -> str | None:
    """Rótulo da legenda para a cor da célula: igual, ou a mais próxima sem ambiguidade."""
    if cor is None or not legenda:
        return None
    for c, lab in legenda.items():
        if _mesma_cor(c, cor):
            return lab
    dist = sorted((sum((a - b) ** 2 for a, b in zip(c, cor)) ** 0.5, lab) for c, lab in legenda.items())
    if dist[0][0] <= 0.45 and (len(dist) == 1 or dist[1][0] >= 2 * dist[0][0] + 0.2):
        return dist[0][1]
    return None


def _cor_celula(x, y, fills) -> tuple | None:
    dentro = [(r, c) for r, c in fills if r.x0 - 0.5 <= x <= r.x1 + 0.5 and r.y0 - 0.5 <= y <= r.y1 + 0.5]
    if not dentro:
        return None
    return min(dentro, key=lambda rc: rc[0].get_area())[1]


def parse_pagina(page, pno: int) -> GabaritoPagina:
    words, origem = _palavras(page)
    g = GabaritoPagina(pno, origem=origem)
    linhas = _linhas(words)
    texto = "\n".join(" ".join(w[4] for w in lw) for _, lw in linhas)
    g.texto_cabecalho = texto
    tn = norm(texto)
    if "PRELIMINAR" in tn:
        g.fase = "preliminar"
    if "DEFINITIV" in tn:
        g.fase = "definitivo" if g.fase is None else None   # ambos => ambíguo
    m = _COD.search(texto.replace(" ", "")) or _COD.search(texto)
    if m:
        g.codigo_prova = m.group(1).upper()
    m = re.search(r"\bCADERNO\s+([A-ZÀ-Ü]{3,})\b", texto, re.I)
    if m and m.group(1).upper() not in ("DE",):
        g.caderno = m.group(1).upper()
    m = re.search(r"^(CARGO\s*\d+.*|[ÁA]REA\s*\d+.*)$", texto, re.I | re.M)
    if m:
        g.cargo = m.group(1).strip()
    g.data_edital = anos.data_edital_texto(tn)
    g.data_aplicacao = anos.data_aplicacao_texto(texto)

    conflitos: set[int] = set()
    fills = _preenchimentos(page) if origem == "pdf" else []
    legenda = _legenda(linhas, fills) if fills else {}
    for i, (yc, lw) in enumerate(linhas):
        nums = _linha_numeros(lw)
        if not nums:
            continue
        passo = statistics.median([b[0] - a[0] for a, b in zip(nums, nums[1:])]) if len(nums) > 1 else 20
        # próxima linha abaixo com tokens de resposta
        resp_linha = None
        for yc2, lw2 in linhas[i + 1:i + 4]:
            if yc2 - yc > 40:
                break
            toks = [w for w in lw2 if _eh_resposta(w[4])]
            if len(toks) >= max(1, 0.5 * len(lw2)):
                resp_linha = toks
                break
        if resp_linha is None:
            g.avisos.append(f"linha de itens sem respostas (p.{pno + 1}, itens {nums[0][4]}–{nums[-1][4]})")
            continue
        for n in nums:
            cx = (n[0] + n[2]) / 2
            cel = [w for w in resp_linha if abs((w[0] + w[2]) / 2 - cx) <= passo * 0.45]
            toks = [w[4].upper() for w in cel if w[4].upper() in RESPOSTAS]
            if not toks:
                continue
            r = "X" if "X" in toks else toks[0]
            num = int(n[4])
            cor = _cor_celula(cx, (n[1] + n[3]) / 2, fills) if legenda else None
            rot = _rotulo(cor, legenda)
            if rot:
                alvo = g.variantes.setdefault(rot, {})
                if num in alvo and alvo[num] != r:
                    g.avisos.append(f"item {num} ({rot}) com duas respostas; deixado sem resposta")
                    alvo.pop(num, None)
                    continue
                alvo[num] = r
                continue
            if num in g.respostas and g.respostas[num] != r:
                conflitos.add(num)
            g.respostas[num] = r
    if conflitos:
        if len(conflitos) > 0.3 * max(1, len(g.respostas)):
            g.avisos.append(f"tabela não confiável: {len(conflitos)} itens com respostas conflitantes; descartada")
            g.respostas = {}
        else:
            for num in sorted(conflitos):
                g.respostas.pop(num, None)
            g.avisos.append(f"itens {sorted(conflitos)} com respostas diferentes na mesma página "
                            f"(ex.: opções de língua estrangeira); deixados sem resposta")
    return g


def parse(caminho: Path | str) -> list[GabaritoPagina]:
    out = []
    with pymupdf.open(caminho) as pdf:
        for pno, page in enumerate(pdf):
            g = parse_pagina(page, pno)
            if g.respostas or g.variantes:
                out.append(g)
    return out


def parse_todas(caminho: Path | str) -> list[GabaritoPagina]:
    with pymupdf.open(caminho) as pdf:
        return [parse_pagina(page, pno) for pno, page in enumerate(pdf)]


def agrupa(paginas: list[GabaritoPagina]) -> list[GabaritoPagina]:
    """Junta páginas consecutivas do mesmo gabarito (mesmo código/caderno ou sem cabeçalho próprio)."""
    res: list[GabaritoPagina] = []
    for g in paginas:
        if res and (g.codigo_prova in (None, res[-1].codigo_prova)) and g.caderno in (None, res[-1].caderno) \
                and not (set(g.respostas) & set(res[-1].respostas)):
            res[-1].respostas.update(g.respostas)
            for k, v in g.variantes.items():
                res[-1].variantes.setdefault(k, {}).update(v)
            res[-1].avisos += g.avisos
        else:
            res.append(g)
    return res
