"""Parse dos gabaritos oficiais (grade Item/Gabarito) por coordenadas, com OCR de fallback."""
from __future__ import annotations

import logging
import re
import shutil
import statistics
import subprocess
import tempfile
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


_ROTULO = re.compile(r"(?i)quest[ãa]o|itens?|item")


def _linha_numeros(lw) -> list | None:
    nums = [w for w in lw if re.fullmatch(r"\d{1,3}", w[4]) and int(w[4]) > 0]
    # rótulo da linha ("Questão", "Item") não conta: "Questão 59 60 0 0 ..." é a última linha, completada com zeros
    rotulo = [w for w in lw if _ROTULO.fullmatch(w[4])]
    outros = [w for w in lw if w[4] not in _VAZIO and w not in rotulo]
    # "Questão 100 0 0 0 ...": um único item na última linha, com rótulo e o resto preenchido com zeros
    unico = len(nums) == 1 and rotulo and len(outros) == 1 and len(lw) > 3
    if (len(nums) < 2 and not unico) or len(nums) < 0.7 * len(outros):
        return None
    vals = [int(w[4]) for w in nums]
    crescente = sum(1 for a, b in zip(vals, vals[1:]) if b == a + 1)
    if crescente < 0.7 * (len(vals) - 1):
        return None
    return nums


def _eh_resposta(tok: str, ocr: bool = False) -> bool:
    return _letra(tok, ocr) is not None or tok in _VAZIO


def _letra(tok: str, ocr: bool = False) -> str | None:
    """Resposta de uma célula. No OCR, aceita a letra repetida que ele produz ('Cc' = C, 'XxX' = X)."""
    s = tok.upper()
    if s in RESPOSTAS:
        return s
    if ocr and 1 < len(s) <= 3 and len(set(s)) == 1 and s[0] in RESPOSTAS:
        return s[0]
    return None


def _numera_por_posicao(lw, nums, passo: float) -> list[tuple]:
    """OCR lê '11' como '1', '41' como '411', '70' como '7O'. Numa grade regular, o número de cada célula sai da
    posição: ajusta valor = base + (x - x0)/passo pela mediana dos números legíveis e numera todos os tokens da linha
    à direita do rótulo. Devolve [(token, número)]; vazio se os números legíveis não forem coerentes com a grade."""
    cx = lambda w: (w[0] + w[2]) / 2  # noqa: E731
    x0 = cx(nums[0])
    base = statistics.median(int(w[4]) - (cx(w) - x0) / passo for w in nums)
    coerentes = sum(1 for w in nums if abs(int(w[4]) - (base + (cx(w) - x0) / passo)) < 0.3)
    if coerentes < 0.7 * len(nums):
        return []
    out, vistos = [], set()
    for w in lw:
        if cx(w) < x0 - passo * 0.5 or w[4] in _VAZIO:
            continue                                   # rótulo "Questão"; células vazias ("0") de preenchimento
        pos = base + (cx(w) - x0) / passo
        v = round(pos)
        if abs(pos - v) > 0.3 or v <= 0 or v in vistos:
            continue
        vistos.add(v)
        out.append((w, v))
    return out


_TESSERACT: str | None = None


def _tesseract() -> str | None:
    global _TESSERACT
    if _TESSERACT is None:
        cand = shutil.which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        _TESSERACT = cand if Path(cand).exists() else ""
    return _TESSERACT or None


def _ocr_celula(page, rect) -> str | None:
    """OCR de uma única célula (modo caractere isolado), para letras que o OCR da página perdeu."""
    exe = _tesseract()
    if not exe:
        return None
    pix = page.get_pixmap(dpi=400, clip=rect, colorspace=pymupdf.csGRAY)
    with tempfile.TemporaryDirectory() as tmp:
        img = Path(tmp) / "c.png"
        pix.save(img)
        try:
            out = subprocess.run([exe, str(img), "stdout", "--psm", "10", "-c", "tessedit_char_whitelist=ABCDEX"],
                                 capture_output=True, text=True, timeout=30).stdout
        except (OSError, subprocess.SubprocessError):
            return None
    s = re.sub(r"[^A-Z]", "", out.upper())
    return s if len(s) == 1 and s in RESPOSTAS else None


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


_SECAO = re.compile(r"\bCADERNO\s*(\d{1,2}\.\d{1,2})\b", re.I)
_ALTERACAO = re.compile(
    r"QUEST[ÃA]O\s+(\d{1,3})\s+(ANULADA|ALTERADA\s+DE\s+([A-E])\s+P/\s*([A-E]))\s+VERS[ÃA]O\s+DE\s+PROVA\s+(\d{1,2}\.\d{1,2})",
    re.I)


def _secoes(linhas) -> list[tuple[str | None, list]]:
    """Divide a página em seções por cabeçalho 'CadernoX.Y' (ex.: gabaritos publicados em diário oficial, um bloco
    por versão da prova). Sem ao menos dois cabeçalhos distintos, a página inteira é uma seção."""
    marcas = []
    for i, (_, lw) in enumerate(linhas):
        m = _SECAO.search(" ".join(w[4] for w in lw).replace("Caderno ", "Caderno"))
        if m:
            marcas.append((i, m.group(1)))
    if len({rot for _, rot in marcas}) < 2:
        return [(None, linhas)]
    out = []
    for k, (i, rot) in enumerate(marcas):
        fim = marcas[k + 1][0] if k + 1 < len(marcas) else len(linhas)
        out.append((rot, _recorta_coluna(linhas[i:fim])))
    return out


def _recorta_coluna(linhas) -> list:
    """Página de jornal: a mesma altura tem texto de outras colunas. Mantém só a faixa x da tabela, delimitada pela
    sequência contínua de números (1, 2, 3, ...) da primeira linha de itens."""
    for _, lw in linhas:
        nums = [w for w in lw if re.fullmatch(r"\d{1,3}", w[4])]
        run = nums[:1]
        for w in nums[1:]:
            passo = run[-1][2] - run[-1][0] + 12 if len(run) < 2 else 2.5 * (run[-1][0] - run[-2][0])
            if int(w[4]) == int(run[-1][4]) + 1 and w[0] - run[-1][0] <= passo:
                run.append(w)
            elif len(run) >= 5:
                break
            else:
                run = [w]
        if len(run) >= 5:
            rotulo = [w for w in lw if w[2] <= run[0][0] and run[0][0] - w[2] < 40]   # "Questão"
            x0 = min([w[0] for w in rotulo] + [run[0][0]]) - 1
            x1 = run[-1][2] + 0.5 * (run[-1][0] - run[-2][0])
            return [(yc, f) for yc, l in linhas if (f := [w for w in l if x0 <= w[0] and w[2] <= x1])]
    return linhas


def alteracoes(texto: str) -> dict[str, dict[int, tuple[str | None, str]]]:
    """Lista 'Questão N / Anulada | Alterada de X p/ Y / Versão de prova V' -> {versão: {item: (antes, depois)}}.
    'depois' = 'X' para anulada."""
    out: dict[str, dict[int, tuple[str | None, str]]] = {}
    for m in _ALTERACAO.finditer(re.sub(r"\s+", " ", texto)):
        num, versao = int(m.group(1)), m.group(5)
        antes, depois = (None, "X") if m.group(2).upper().startswith("ANULADA") else (m.group(3).upper(), m.group(4).upper())
        out.setdefault(versao, {})[num] = (antes, depois)
    return out


def parse_pagina(page, pno: int) -> list[GabaritoPagina]:
    words, origem = _palavras(page)
    linhas = _linhas(words)
    secoes = _secoes(linhas)
    if len(secoes) == 1:
        return [_parse_linhas(page, pno, words, origem, linhas)]
    out = []
    for rot, ls in secoes:
        g = _parse_linhas(page, pno, words, origem, ls, texto_pagina=linhas)
        g.caderno = rot or g.caderno
        # página de diário oficial: o texto ao redor é de outras matérias; a fase vem da classificação do documento
        g.fase = None
        g.codigo_prova = None
        if rot or g.respostas:
            out.append(g)
    return out


def _parse_linhas(page, pno: int, words, origem: str, linhas, texto_pagina=None) -> GabaritoPagina:
    g = GabaritoPagina(pno, origem=origem)
    texto = "\n".join(" ".join(w[4] for w in lw) for _, lw in (texto_pagina or linhas))
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
        resp_linha, resp_y = None, None
        for yc2, lw2 in linhas[i + 1:i + 4]:
            if yc2 - yc > 40:
                break
            toks = [w for w in lw2 if _eh_resposta(w[4], origem == "ocr")]
            if len(toks) >= max(1, 0.5 * len(lw2)):
                resp_linha, resp_y = lw2, yc2
                break
        if resp_linha is None:
            g.avisos.append(f"linha de itens sem respostas (p.{pno + 1}, itens {nums[0][4]}–{nums[-1][4]})")
            continue
        celulas = []
        if origem == "ocr":
            celulas = _numera_por_posicao(lw, nums, passo)
        elif len(nums) >= 2 and any(w not in nums and w[4] not in _VAZIO and not _ROTULO.fullmatch(w[4]) for w in lw):
            # célula de número corrompida no próprio PDF (ex.: 'X05' no lugar de 50): numera pela posição na grade
            celulas = _numera_por_posicao(lw, nums, passo)
            extras = sorted(v for w, v in celulas if w not in nums)
            if extras:
                g.avisos.append(f"itens {extras} numerados pela posição (célula de número ilegível no PDF)")
        celulas = celulas or [(n, int(n[4])) for n in nums]
        for n, num in celulas:
            cx = (n[0] + n[2]) / 2
            cel = [w for w in resp_linha if abs((w[0] + w[2]) / 2 - cx) <= passo * 0.45]
            toks = [x for w in cel if (x := _letra(w[4], origem == "ocr"))]
            if not toks and origem == "ocr":
                h = max(6.0, n[3] - n[1])
                r_ocr = _ocr_celula(page, pymupdf.Rect(cx - passo * 0.45, resp_y - h, cx + passo * 0.45, resp_y + h))
                toks = [r_ocr] if r_ocr else []
            if not toks:
                continue
            r = "X" if "X" in toks else toks[0]
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
            out += [g for g in parse_pagina(page, pno) if g.respostas or g.variantes]
    return out


def texto_leitura(caminho: Path | str) -> str:
    """Texto na ordem de leitura (blocos/colunas), para listas corridas como a de alterações."""
    with pymupdf.open(caminho) as pdf:
        return "\n".join(page.get_text() for page in pdf)


def parse_todas(caminho: Path | str) -> list[GabaritoPagina]:
    with pymupdf.open(caminho) as pdf:
        return [g for pno, page in enumerate(pdf) for g in parse_pagina(page, pno)]


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
