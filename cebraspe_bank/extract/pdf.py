"""Leitura de PDF em linhas com coordenadas, ordem de leitura por colunas e OCR de fallback."""
from __future__ import annotations

import collections
import logging
import re
import shutil
import statistics
import subprocess
import tempfile
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


_TESSERACT: str | None = None


def _tesseract() -> str | None:
    global _TESSERACT
    if _TESSERACT is None:
        cand = shutil.which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        _TESSERACT = cand if Path(cand).exists() else ""
    return _TESSERACT or None


def ocr_recorte(page, rect, whitelist: str, psm: int = 8, dpi: int = 400) -> str | None:
    """OCR de um recorte pequeno da página (célula, número de item) restrito a `whitelist`, com o executável do
    Tesseract (o OCR de página inteira perde caracteres isolados e números em negrito encostados em fios)."""
    exe = _tesseract()
    if not exe:
        return None
    pix = page.get_pixmap(dpi=dpi, clip=rect, colorspace=pymupdf.csGRAY)
    with tempfile.TemporaryDirectory() as tmp:
        img = Path(tmp) / "c.png"
        pix.save(img)
        try:
            return subprocess.run([exe, str(img), "stdout", "--psm", str(psm), "-c",
                                   f"tessedit_char_whitelist={whitelist}"],
                                  capture_output=True, text=True, timeout=30).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None


def _eh_capa_instrucoes(texto: str) -> bool:
    """Capa do caderno: instruções ao candidato ('Ao receber este caderno...', 'aplicador de provas'), sem itens."""
    t = texto.upper()
    sinais = sum(bool(re.search(p, t)) for p in (r"AO RECEBER ESTE CADERNO", r"INSTRU[ÇC][ÕO]ES", r"APLICADOR",
                                                 r"FOLHA DE RESPOSTAS", r"DURA[ÇC][ÃA]O DA[S]? PROVA"))
    return sinais >= 3 and not re.search(r"JULGUE OS (ITENS|PR[ÓO]XIMOS)|ASSINALE A OP[ÇC][ÃA]O", t)


def _tira_fio(w):
    """'|Com' -> 'Com' com a caixa encolhida na proporção dos caracteres (fio do scan colado à palavra)."""
    t = w[4]
    ini = len(t) - len(t.lstrip("|¦"))
    fim = len(t) - len(t.rstrip("|¦"))
    if not (ini or fim) or ini + fim >= len(t):
        return w
    larg = (w[2] - w[0]) / len(t)
    return (w[0] + ini * larg, w[1], w[2] - fim * larg, w[3], t[ini:len(t) - fim], *w[5:])


def _corrige_numeros_ocr(page, partes_por_linha: list) -> None:
    """Páginas OCR: a primeira palavra curta de uma linha recuada à esquerda da margem da coluna é o número do item
    (negrito, às vezes encostado num fio do scan) e sai como '&', 'É', 'g', '7º'. Refaz o OCR só desse recorte,
    aceitando apenas dígitos. Altera as listas de palavras no lugar."""
    xs = collections.defaultdict(list)
    for partes in partes_por_linha:
        for col, ws in partes:
            xs[col].append(round(ws[0][0]))
    margem = {col: collections.Counter(v).most_common(1)[0][0] for col, v in xs.items() if v}
    for partes in partes_por_linha:
        for col, ws in partes:
            w = ws[0]
            m = re.fullmatch(r"(\d{1,3})[º°.,]", w[4])
            if m and col in margem and w[0] <= margem[col] - 8:
                ws[0] = (w[0], w[1], w[2], w[3], m.group(1), *w[5:])     # '7º' -> '7'
                continue
            if col not in margem or w[0] > margem[col] - 8 or margem[col] - w[0] > 60 or len(w[4]) > 3 \
                    or re.fullmatch(r"\d{1,3}", w[4]) or len(ws) < 3:
                continue
            r = pymupdf.Rect(w[0] - 2, w[1] - 2, w[2] + 2, w[3] + 2)
            dig = re.sub(r"\D", "", ocr_recorte(page, r, "0123456789") or "")
            if 1 <= len(dig) <= 3:
                ws[0] = (w[0], w[1], w[2], w[3], dig, *w[5:])


def _palavras_pagina(page, ocr: bool):
    if ocr:
        tp = page.get_textpage_ocr(language="por", dpi=300, full=True)
        return page.get_text("words", textpage=tp)
    return page.get_text("words")


def _agrupa_linhas(words, tol=3.0):
    """words -> linhas físicas: mesma linha se o centro está a <= tol ou há sobreposição vertical >= 60%."""
    if words:
        # glifos de fórmula (Cambria Math etc.) têm caixa de várias linhas de altura e fundiriam linhas vizinhas:
        # para o agrupamento, valem com a altura mediana, centrados na caixa original
        h = statistics.median(w[3] - w[1] for w in words)
        words = [w if w[3] - w[1] <= 2.5 * h else
                 (w[0], (w[1] + w[3]) / 2 - h / 2, w[2], (w[1] + w[3]) / 2 + h / 2, *w[4:]) for w in words]
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
    """x da margem esquerda da coluna direita.

    Candidatos: x0 que se repetem na faixa central (margem frequente; >=3 palavras, senão >=2). Escolhe-se o
    menor x entre os que têm quase o mínimo de palavras atravessando a calha (títulos de largura total
    atravessam qualquer x, por isso a tolerância)."""
    xs = collections.Counter(round(w[0]) for w in words if 0.40 * W <= w[0] <= 0.62 * W)
    cands = [x for x, n in xs.items() if n >= 3] or [x for x, n in xs.items() if n >= 2]
    if not cands:
        return W / 2
    cruz = {x: sum(1 for w in words if w[0] < x - 3 and w[2] > x - 1) for x in cands}
    m = min(cruz.values())
    if m > max(2, 0.03 * len(words)):
        return W / 2
    tol = max(2, int(0.01 * len(words)))
    return float(min(x for x in cands if cruz[x] <= m + tol))


def _cruzamentos(words, x: float) -> int:
    return sum(1 for w in words if w[0] < x - 3 and w[2] > x - 1)


def _divisor_documento(paginas_words: list, W: float) -> float | None:
    """Margem da coluna direita mais comum entre as páginas (as colunas são as mesmas no caderno inteiro)."""
    divs = [round(_divisor(ws, W)) for ws in paginas_words if ws]
    divs = [d for d in divs if abs(d - W / 2) > 1]
    if not divs:
        return None
    x, n = collections.Counter(divs).most_common(1)[0]
    return float(x) if n >= 2 else None


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
        pular_capa_sem_texto: bool = True, colunas: bool = True) -> Documento:
    """colunas=False: lê a página inteira como uma coluna (tabelas de justificativa, padrões de resposta)."""
    caminho = Path(caminho)
    pdf = pymupdf.open(caminho)
    doc = Documento(caminho, n_paginas=pdf.page_count)
    tem_texto = [len(pg.get_text().strip()) >= MIN_CHARS_PAGINA for pg in pdf]
    div_doc = _divisor_documento([pg.get_text("words") for pg in pdf], pdf[0].rect.width) if pdf.page_count else None
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
                if pno == 0 and pular_capa_sem_texto and _eh_capa_instrucoes(" ".join(w[4] for w in words)):
                    # caderno todo escaneado: a capa (instruções numeradas 1, 2, 3...) não é conteúdo
                    doc.paginas_sem_texto.append(pno)
                    continue
                doc.paginas_ocr.append(pno)
            except Exception as e:  # noqa: BLE001
                log.warning("OCR falhou em %s p.%d: %s", caminho.name, pno + 1, e)
        origem = "ocr" if ocr else "pdf"
        spans = [] if ocr else _spans(page)
        if ocr:
            words = [w for w in words if not re.fullmatch(r"[|¦]{1,2}", w[4])]   # fio vertical do scan
            words = [_tira_fio(w) for w in words]
        # marcas de controle em fonte minúscula (ex.: <AGEPAR233001A01E2048>) não são conteúdo
        words = [w for w in words if not ((w[3] - w[1]) < 5.0 and re.fullmatch(r"<[^>]*>?|<?[^<>]*>", w[4]))]
        fis = _agrupa_linhas(words)
        corte = 0.0
        for lw in fis:
            y0 = min(w[1] for w in lw)
            if y0 > 70:
                break
            t = _texto(lw)
            if y0 < cabecalho_y and (re.search(r"CEBRASPE\s*[–-]|CESPE\s*\|", t) or
                                     re.fullmatch(r"\|\|[0-9A-Z_]+N\d{4,}\|\|.*", t) or
                                     (_lixo(t) and not re.fullmatch(r"\|\|[A-Z]+\|\|", t))):
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
        ws_corpo = [w for lw in corpo for w in lw]
        meio = _divisor(ws_corpo, W)
        if div_doc is not None and meio != div_doc:
            # sem palavra alinhada na margem do documento (coluna direita que começa com gráfico/fórmula), a margem
            # do documento só vale se não cruzar mais palavras que a da página
            alinhado = any(abs(w[0] - div_doc) <= 2 for w in ws_corpo)
            tol = max(2, int(0.01 * len(ws_corpo))) if alinhado else 0
            if _cruzamentos(ws_corpo, div_doc) <= _cruzamentos(ws_corpo, meio) + tol:
                meio = div_doc
        duas = colunas and _detecta_duas_colunas(corpo, meio)
        segs: list[Linha] = []
        partes_por_linha = [[(c, list(ws)) for c, ws in (_quebra_por_gutter(lw, meio, gap_min=1.0 if ocr else 6.0) if duas else [(-1, lw)])]
                            for lw in corpo]
        if ocr and colunas:
            _corrige_numeros_ocr(page, partes_por_linha)
        for partes in partes_por_linha:
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
