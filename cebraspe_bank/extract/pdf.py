"""Leitura de PDF em linhas com coordenadas, ordem de leitura por colunas e OCR de fallback."""
from __future__ import annotations

import collections
import logging
import re
import statistics
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

log = logging.getLogger(__name__)

MIN_CHARS_PAGINA = 40          # abaixo disso a página é considerada sem camada de texto
HEADER_Y = 46                  # faixa do cabeçalho (código de barras e "CEBRASPE – X – Edital: AAAA")


@dataclass
class Linha:
    pagina: int
    col: int                   # 0 = esquerda, 1 = direita, -1 = largura total
    x0: float
    y0: float
    x1: float
    y1: float
    texto: str
    tamanho: float = 0.0
    origem: str = "pdf"        # pdf | ocr
    fonte0: str = ""           # fonte do primeiro token da linha
    tam0: float = 0.0          # tamanho do primeiro token
    fonte1: str = ""           # fonte do segundo token
    tam1: float = 0.0

    @property
    def palavras(self) -> list[str]:
        return self.texto.split()


@dataclass
class Documento:
    caminho: Path
    linhas: list[Linha] = field(default_factory=list)          # corpo, em ordem de leitura
    cabecalho: list[str] = field(default_factory=list)         # linhas do topo das páginas
    graficos: dict[int, list[pymupdf.Rect]] = field(default_factory=dict)  # imagens/desenhos relevantes
    paginas_ocr: list[int] = field(default_factory=list)
    paginas_sem_texto: list[int] = field(default_factory=list)
    n_paginas: int = 0
    largura: float = 595.0

    @property
    def texto(self) -> str:
        return "\n".join(l.texto for l in self.linhas)

    @property
    def texto_completo(self) -> str:
        return "\n".join(self.cabecalho) + "\n" + self.texto


_LIXO = re.compile(r"^\|\|.*\|\|$|^[\w`^~]{12,}$")


def _lixo(t: str) -> bool:
    """Código de barras e textos ofuscados (ex.: '||234INSS_001_01N297373||', 'Tfe_VT`dVeqfpSp`Tfp')."""
    s = t.strip()
    if not s:
        return True
    if s.startswith("||") and s.endswith("||") and " " not in s:
        return not re.fullmatch(r"\|\|[A-Z]\|\||\|\|JUSTIFICATIVAS?\|\|", s)
    if "`" in s or (re.fullmatch(r"[A-Za-z0-9_`^~]{14,}", s) and re.search(r"[a-z][A-Z]|[A-Z]{2}[a-z][A-Z]|_", s)
                    and not re.search(r"[aeiouáéíóú]{1}[a-z]{2,}", s)):
        return True
    return False


def _palavras_pagina(page, ocr: bool):
    if ocr:
        tp = page.get_textpage_ocr(language="por", dpi=300, full=True)
        return page.get_text("words", textpage=tp)
    return page.get_text("words")


def _agrupa_linhas(words, tol=3.0):
    """words -> linhas físicas: mesma linha se o centro está a <= tol ou há sobreposição vertical >= 60%."""
    ws = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    linhas: list[list] = []          # [y0, y1, [words]]
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if linhas:
            y0, y1, lw = linhas[-1]
            lc = (y0 + y1) / 2
            sob = min(y1, w[3]) - max(y0, w[1])
            menor = max(0.1, min(y1 - y0, w[3] - w[1]))
            if abs(lc - yc) <= tol or sob / menor >= 0.6:
                lw.append(w)
                linhas[-1][0], linhas[-1][1] = min(y0, w[1]), max(y1, w[3])
                continue
        linhas.append([w[1], w[3], [w]])
    return [sorted(lw, key=lambda w: w[0]) for _, _, lw in linhas]


def _divisor(words, W: float) -> float:
    """x da margem esquerda da coluna direita: x0 frequente na faixa central que quase nenhuma palavra atravessa."""
    xs = collections.Counter(round(w[0]) for w in words if 0.40 * W <= w[0] <= 0.62 * W)
    melhor = None
    for x, n in xs.items():
        if n < 3:
            continue
        cruz = sum(1 for w in words if w[0] < x - 3 and w[2] > x - 1)
        chave = (cruz, x)          # sem cruzamentos; empate -> a menor x (margem, não o recuo)
        if melhor is None or chave < melhor[0]:
            melhor = (chave, x)
    if melhor and melhor[0][0] <= max(2, 0.02 * len(words)):
        return float(melhor[1])
    return W / 2


def _quebra_por_gutter(lw, meio: float, gap_min=6.0):
    """Divide uma linha física em segmentos de coluna; `meio` é a margem esquerda da coluna direita."""
    esq = [w for w in lw if w[2] <= meio - 1]
    dir_ = [w for w in lw if w[0] >= meio - 3]
    cruza = [w for w in lw if w[0] < meio - 3 and w[2] > meio - 1]
    if cruza:
        return [(-1, lw)]
    if esq and dir_:
        if dir_[0][0] - esq[-1][2] >= gap_min:
            return [(0, esq), (1, dir_)]
        return [(-1, lw)]
    if esq:
        return [(0, esq)]
    return [(1, dir_)]


def _spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type"):
            continue
        for l in b["lines"]:
            for sp in l["spans"]:
                if sp["text"].strip():
                    out.append((pymupdf.Rect(sp["bbox"]), sp["font"], sp["size"]))
    return out


def _fonte_de(w, spans):
    cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
    for r, f, sz in spans:
        if r.x0 - 0.5 <= cx <= r.x1 + 0.5 and r.y0 - 0.5 <= cy <= r.y1 + 0.5:
            return f, sz
    return "", 0.0


def _texto(lw) -> str:
    return re.sub(r"\s+", " ", " ".join(w[4] for w in lw)).strip()


def _detecta_duas_colunas(linhas_fis, meio: float) -> bool:
    n_esq = n_dir = n_cruza = 0
    for lw in linhas_fis:
        for col, _ in _quebra_por_gutter(lw, meio):
            if col == 0:
                n_esq += 1
            elif col == 1:
                n_dir += 1
            else:
                n_cruza += 1
    return n_esq >= 3 and n_dir >= 3 and n_cruza <= 0.35 * (n_esq + n_dir + n_cruza)


def _graficos(page) -> list[pymupdf.Rect]:
    """Imagens e grupos de desenho vetorial (tabelas, gráficos) com área relevante."""
    rects: list[pymupdf.Rect] = []
    W, H = page.rect.width, page.rect.height
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"]) & page.rect
        if r.get_area() >= 3000 and r.y0 > HEADER_Y:
            rects.append(r)
    try:
        for g in page.cluster_drawings():
            r = pymupdf.Rect(g) & page.rect
            if r.width > 0.9 * W or r.height > 0.9 * H:   # molduras e fios de página
                continue
            if r.get_area() >= 4000 and r.width > 40 and r.height > 25 and r.y0 > HEADER_Y:
                rects.append(r)
    except Exception:  # noqa: BLE001 — versões antigas do PyMuPDF
        pass
    return rects


def ler(caminho: Path | str, forcar_ocr: bool = False, cabecalho_y: float = HEADER_Y,
        pular_capa_sem_texto: bool = True) -> Documento:
    caminho = Path(caminho)
    pdf = pymupdf.open(caminho)
    doc = Documento(caminho, n_paginas=pdf.page_count)
    tem_texto = [len(pg.get_text().strip()) >= MIN_CHARS_PAGINA for pg in pdf]
    for pno, page in enumerate(pdf):
        W = page.rect.width
        doc.largura = W
        words = _palavras_pagina(page, False)
        ocr = forcar_ocr or sum(len(w[4]) for w in words) < MIN_CHARS_PAGINA
        if ocr and not forcar_ocr and pno == 0 and any(tem_texto[1:]) and pular_capa_sem_texto:
            doc.paginas_sem_texto.append(pno)   # capa sem texto: não vira conteúdo
            continue
        if ocr:
            try:
                words = _palavras_pagina(page, True)
                doc.paginas_ocr.append(pno)
            except Exception as e:  # noqa: BLE001
                log.warning("OCR falhou em %s p.%d: %s", caminho.name, pno + 1, e)
        origem = "ocr" if ocr else "pdf"
        spans = [] if ocr else _spans(page)
        # marcas de controle em fonte minúscula (ex.: <AGEPAR233001A01E2048>) não são conteúdo
        words = [w for w in words if not ((w[3] - w[1]) < 5.0 and re.fullmatch(r"<[^>]*>?|<?[^<>]*>", w[4]))]
        fis = _agrupa_linhas(words)
        corte = 0.0
        for lw in fis:
            y0 = min(w[1] for w in lw)
            if y0 > 70:
                break
            t = _texto(lw)
            if re.search(r"CEBRASPE|CESPE|^\|\|\S+\|\|$", t) or (_lixo(t) and y0 < cabecalho_y):
                corte = max(corte, max(w[3] for w in lw) + 1.0)
        corpo = []
        for lw in fis:
            y0 = min(w[1] for w in lw)
            t = _texto(lw)
            if y0 < corte:
                doc.cabecalho.append(t)
                continue
            if _lixo(t):
                continue
            if statistics.median(w[3] - w[1] for w in lw) < 5.0 and re.fullmatch(r"<[^>]+>|\S+", t):
                continue          # marcas de controle em fonte minúscula (ex.: <AGEPAR233001A01E2048>)
            corpo.append(lw)
        meio = _divisor([w for lw in corpo for w in lw], W)
        duas = _detecta_duas_colunas(corpo, meio)
        segs: list[Linha] = []
        for lw in corpo:
            partes = _quebra_por_gutter(lw, meio) if duas else [(-1, lw)]
            for col, ws in partes:
                t = _texto(ws)
                if not t or _lixo(t):
                    continue
                f0, s0 = _fonte_de(ws[0], spans) if spans else ("", 0.0)
                f1, s1 = _fonte_de(ws[1], spans) if spans and len(ws) > 1 else ("", 0.0)
                segs.append(Linha(pno, col, min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws),
                                  max(w[3] for w in ws), t, statistics.median(w[3] - w[1] for w in ws), origem,
                                  f0, s0, f1, s1))
        # ordem de leitura: faixas separadas por linhas de largura total; em cada faixa, esquerda e depois direita
        ordenado: list[Linha] = []
        faixa: list[Linha] = []

        def fecha():
            ordenado.extend(sorted([l for l in faixa if l.col == -1], key=lambda l: l.y0))
            ordenado.extend(sorted([l for l in faixa if l.col == 0], key=lambda l: l.y0))
            ordenado.extend(sorted([l for l in faixa if l.col == 1], key=lambda l: l.y0))
            faixa.clear()

        for l in sorted(segs, key=lambda l: l.y0):
            if l.col == -1 and duas:
                fecha()
                ordenado.append(l)
            else:
                faixa.append(l)
        fecha()
        doc.linhas.extend(ordenado)
        doc.graficos[pno] = _graficos(page) if not ocr else []
    pdf.close()
    return doc


def recorte(caminho: Path | str, pagina: int, rect: pymupdf.Rect, destino: Path, dpi: int = 150) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(caminho) as pdf:
        pix = pdf[pagina].get_pixmap(clip=rect, dpi=dpi)
        pix.save(destino)
    return destino
