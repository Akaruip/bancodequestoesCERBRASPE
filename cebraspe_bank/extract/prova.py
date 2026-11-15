"""Segmentação de cadernos de prova em textos-base, itens C/E, questões de múltipla escolha e discursivas."""
from __future__ import annotations

import collections
import dataclasses
import re
import statistics
from dataclasses import dataclass, field

from .pdf import Documento, Linha

_SECAO = re.compile(r"^-{2,}\s*(.+?)\s*(?:-{2,}|[–—])$")
_QUESTAO = re.compile(r"^QUEST[ÃA]O\s+(?:[^\d\s]{1,2}\s+)?(\d{1,3})\b\s*(.*)$", re.I)
_ALT = re.compile(r"^([A-E])\s+(\S.*)$")
_FAIXA = re.compile(r"(?:itens|quest[õo]es)\s+(?:de\s+)?(\d{1,3})\s+(?:a|e)\s+(\d{1,3})", re.I)
_JUST = re.compile(r"^\|\|JUSTIFICATIVAS?\|\|")
_JUST_ALT = re.compile(r"^\|\|([A-E])\|\|\s*-?\s*(.*)$")
_JUST_CE = re.compile(r"^JUSTIFICATIVAS?\s*[-–:]\s*(CERTO|ERRADO|CORRETO|INCORRETO|ANULAD)", re.I)
_LINGUA = re.compile(r"^L[ÍI]NGUA\s+(INGLESA|ESPANHOLA|FRANCESA|ALEM[ÃA]|ITALIANA)\s*$", re.I)
_ESPACO = re.compile(r"^espa[çc]o\s+livre$", re.I)


@dataclass
class Bloco:
    id: int
    linhas: list[Linha] = field(default_factory=list)
    faixa: tuple[int, int] | None = None

    @property
    def texto(self) -> str:
        return junta(self.linhas)

    @property
    def tipo(self) -> str:
        t = self.texto
        if self.faixa or len(t) > 450 or re.match(r"^Texto\b", t):
            return "texto"
        return "comando"


@dataclass
class Item:
    numero: int
    tipo: str                                  # CE | ME | DISC
    linhas: list[Linha] = field(default_factory=list)
    alternativas: dict[str, list[Linha]] = field(default_factory=dict)
    justificativa: list[Linha] = field(default_factory=list)
    bloco: Bloco | None = None
    blocos_anteriores: list[Bloco] = field(default_factory=list)
    secao: str | None = None
    numero_bruto: str = ""
    variante: str = ""                         # opção de língua estrangeira ('' = item comum)

    @property
    def enunciado(self) -> str:
        return junta(self.linhas)

    @property
    def pagina(self) -> int:
        return self.linhas[0].pagina if self.linhas else 0

    def alternativas_texto(self) -> dict[str, str]:
        return {k: junta(v) for k, v in self.alternativas.items()}


@dataclass
class ResultadoProva:
    itens: list[Item]
    blocos: list[Bloco]
    tipo: str                                  # CE | ME | DISC | misto
    cifra: str | None = None                   # mapa glifo->dígito usado nos números ofuscados
    avisos: list[str] = field(default_factory=list)


def norm_lingua(t: str) -> str:
    m = _LINGUA.match(t.strip())
    nome = m.group(1).upper().replace("Ã", "A") if m else t.strip().upper()
    return {"ALEMA": "ALEMÃ"}.get(nome, nome).join(["LÍNGUA ", ""])


def _dig(t: str) -> bool:
    """Só dígitos ASCII (str.isdigit aceita '³', '²' etc.)."""
    return t.isascii() and t.isdigit()


def junta(linhas: list[Linha]) -> str:
    out = ""
    for l in linhas:
        t = l.texto.strip()
        if not t:
            continue
        if not out:
            out = t
        elif out.endswith("-") and not out.endswith(" -") and t[:1].islower():
            out += t
        else:
            out += " " + t
    return out.strip()


def _margens(linhas: list[Linha]) -> dict[tuple[int, int], float]:
    """Margem esquerda por (página, coluna). Usa a margem global da coluna (todas as páginas) quando a página
    tem alguma linha nela; senão, o menor x frequente da própria página."""
    por = collections.defaultdict(list)
    glob_ = collections.defaultdict(list)
    for l in linhas:
        por[(l.pagina, l.col)].append(round(l.x0))
        glob_[l.col].append(round(l.x0))
    g = {}
    for col, xs in glob_.items():
        c = collections.Counter(xs)
        freq = [x for x, n in c.items() if n >= 3]
        if freq:
            g[col] = float(min(freq))
    m = {}
    for k, xs in por.items():
        c = collections.Counter(xs)
        frequentes = [x for x, n in c.items() if n >= 2] or list(c)
        local = float(min(frequentes))
        gc = g.get(k[1])
        if gc is not None and any(abs(x - gc) <= 4 for x in xs):
            m[k] = gc
        else:
            m[k] = local
    return m


def _decodifica(tok: str, k: int) -> int | None:
    ds = []
    for ch in tok:
        d = ord(ch) - k
        if not 0 <= d <= 9:
            return None
        ds.append(str(d))
    return int("".join(ds)) if ds else None


def _instrucoes(linhas: list[Linha]) -> set[int]:
    """Índices das linhas de instruções (parágrafos com '•') — não são conteúdo de questão."""
    fora: set[int] = set()
    i = 0
    while i < len(linhas):
        l = linhas[i]
        if l.texto.startswith("•") or l.texto == "•":
            x_bullet = l.x0
            x_cont = None
            fora.add(i)
            j = i + 1
            while j < len(linhas):
                lj = linhas[j]
                if _SECAO.match(lj.texto) or _QUESTAO.match(lj.texto):
                    break
                continua = (lj.pagina == l.pagina and lj.x0 > x_bullet + 5 and lj.y0 - linhas[j - 1].y1 < 14
                            and (x_cont is None or abs(lj.x0 - x_cont) <= 3))
                if continua and x_cont is None:
                    x_cont = lj.x0
                if lj.texto.startswith("•") or continua:
                    fora.add(j)
                    j += 1
                    continue
                break
            i = j
            continue
        i += 1
    return fora


def _secao(l: Linha) -> str | None:
    m = _SECAO.match(l.texto)
    if m:
        return m.group(1).strip()
    t = l.texto.strip()
    if l.col == -1 and t.isupper() and len(t) < 90 and not _dig(t[:1]) and len(t.split()) <= 10 \
            and re.match(r"^(CONHECIMENTOS|L[ÍI]NGUA|PROVA|PARTE|BLOCO|M[ÓO]DULO|NO[ÇC][ÕO]ES|RACIOC|DIREITO|LEGISLA)", t):
        return t
    return None


def segmentar(doc: Documento, modalidade: str | None = None, esperados: set[int] | None = None) -> ResultadoProva:
    todas = doc.linhas
    fora = _instrucoes(todas)
    linhas = []
    for i, l in enumerate(todas):
        if i in fora or _ESPACO.match(l.texto):
            continue
        if re.search(r"espa[çc]o\s+livre", l.texto, re.I):     # rótulo da outra coluna fundido na linha
            t = re.sub(r"\s*espa[çc]o\s+livre\s*", " ", l.texto, flags=re.I).strip()
            if not t:
                continue
            l = dataclasses.replace(l, texto=t)
        linhas.append(l)
    margens = _margens(linhas)
    avisos: list[str] = []

    def na_margem(l: Linha, tol=3.5) -> bool:
        return abs(l.x0 - margens.get((l.pagina, l.col), l.x0)) <= tol

    # ---------- blocos de opção de língua estrangeira ("LÍNGUA ESPANHOLA", "LÍNGUA INGLESA" ...)
    titulos_lingua = [i for i, l in enumerate(linhas) if _LINGUA.match(l.texto.strip())]
    blocos_lingua: list[tuple[int, int, str]] = []      # (início, fim exclusivo, rótulo)

    lado_a_lado: list[tuple[Linha, str]] = []          # (título, rótulo) quando os blocos ficam em colunas
    numeros_lingua: set[int] = set()

    def rotulo_lingua(i: int, n: int | None = None) -> str:
        if lado_a_lado:
            l = linhas[i]
            for t, lab in lado_a_lado:
                if l.pagina == t.pagina and l.col == t.col and l.y0 >= t.y0 and (n is None or n in numeros_lingua):
                    return lab
            return ""
        for a, b, lab in blocos_lingua:
            if a <= i < b:
                return lab
        return ""

    # ---------- formato de múltipla escolha / discursiva com "Questão N"
    def cab_questao(l: Linha) -> bool:
        m = _QUESTAO.match(l.texto)
        return bool(m) and (na_margem(l, 30) or (not m.group(2) and na_margem(l, 90)))

    n_quest = sum(1 for l in linhas if cab_questao(l))
    formato_me = n_quest >= 1

    def numero_inicio(i: int) -> int | None:
        l = linhas[i]
        if formato_me:
            m = _QUESTAO.match(l.texto)
            return int(m.group(1)) if m and cab_questao(l) else None
        p = l.palavras
        if p and _dig(p[0]) and len(p[0]) <= 3 and na_margem(l) and not (l.tam0 and l.tam0 < 6.5):
            return int(p[0])
        return None

    tl = [linhas[i] for i in titulos_lingua]
    if len(tl) >= 2 and len({(t.pagina, t.col) for t in tl}) == len(tl) and len({t.pagina for t in tl}) == 1 \
            and max(t.y0 for t in tl) - min(t.y0 for t in tl) < 8:
        lado_a_lado = [(t, norm_lingua(t.texto)) for t in tl]
        conj = []
        for t, _ in lado_a_lado:
            conj.append({n for i, l in enumerate(linhas) if l.pagina == t.pagina and l.col == t.col and l.y0 > t.y0
                         for n in [numero_inicio(i)] if n is not None})
        numeros_lingua = set.intersection(*conj) if conj else set()
        if numeros_lingua:
            avisos.append("blocos de língua estrangeira lado a lado: " + ", ".join(lab for _, lab in lado_a_lado))
        else:
            lado_a_lado = []
    elif len(titulos_lingua) >= 2:
        rot = [norm_lingua(linhas[i].texto) for i in titulos_lingua]
        for j, ini in enumerate(titulos_lingua[:-1]):
            blocos_lingua.append((ini, titulos_lingua[j + 1], rot[j]))
        nums_1 = [(i, n, "") for i in range(*blocos_lingua[0][:2]) for n in [numero_inicio(i)] if n is not None]
        seq_1 = _cadeia(nums_1, None, salto_max=1)      # itens do 1º bloco (ignora números soltos do texto)
        kmax = max(n for _, n, _ in seq_1) if seq_1 else None
        fim = len(linhas)
        if kmax is not None:
            for i in range(titulos_lingua[-1] + 1, len(linhas)):
                n = numero_inicio(i)
                if (n is not None and n > kmax) or _secao(linhas[i]):
                    fim = i
                    break
        blocos_lingua.append((titulos_lingua[-1], fim, rot[-1]))
        conjuntos = [{n for _, n, _ in _cadeia([(i, n, "") for i in range(a, b) for n in [numero_inicio(i)]
                                                 if n is not None], None, salto_max=1)}
                     for a, b, _ in blocos_lingua]
        if not conjuntos[0] or not all(c & conjuntos[0] for c in conjuntos[1:]):
            blocos_lingua = []          # numeração não se repete: seções obrigatórias, não opções de língua
        else:
            avisos.append("blocos de língua estrangeira: " + ", ".join(f"{lab}" for _, _, lab in blocos_lingua))

    # ---------- candidatos a início de item C/E
    cands: list[tuple[int, str, str]] = []     # (índice da linha, token, fonte)
    tams = [l.tam1 for l in linhas if l.tam1]
    corpo_tam = statistics.median(tams) if tams else 10.0
    if not formato_me:
        for i, l in enumerate(linhas):
            p = l.palavras
            if not p or not na_margem(l):
                continue
            t0 = p[0]
            if len(p) == 1 and not ((i + 1 < len(linhas) and linhas[i + 1].x0 > l.x0 + 5)
                                    or (l.tam0 and l.tam0 < corpo_tam - 0.8)):
                continue
            if not 1 <= len(t0) <= 3 or (l.tam0 and l.tam0 < 6.5):   # números de linha dos textos são minúsculos
                continue
            fonte_distinta = bool((l.fonte0 and l.fonte1 and l.fonte0 != l.fonte1) or
                                  (l.tam0 and l.tam1 and l.tam0 < l.tam1 - 0.4) or
                                  (len(p) == 1 and l.tam0 and l.tam0 < corpo_tam - 0.8))
            if _dig(t0) or fonte_distinta:
                cands.append((i, t0, l.fonte0))
    cifra = None
    numerados: list[tuple[int, int, str]] = []
    if cands:
        diretos = [(i, int(t), t) for i, t, _ in cands if _dig(t)]
        if blocos_lingua or lado_a_lado:
            rotulos = [lab for _, _, lab in blocos_lingua] or [lab for _, lab in lado_a_lado]
            principal = [x for x in diretos if rotulo_lingua(x[0], x[1]) in ("", rotulos[0])]
            numerados = _cadeia(principal, esperados)
            for lab in rotulos[1:]:
                numerados += _cadeia([x for x in diretos if rotulo_lingua(x[0], x[1]) == lab], None)
            numerados.sort()
        else:
            numerados = _cadeia(diretos, esperados)
        if any(not _dig(t) for _, t, _ in cands):
            mapa = _resolve_substituicao(cands)
            if mapa:
                dec = []
                for i, t, _ in cands:
                    if all(ch in mapa for ch in t):
                        dec.append((i, int("".join(mapa[ch] for ch in t)), t))
                cad = _cadeia(dec, esperados)
                if len(cad) > len(numerados):
                    numerados = cad
                    cifra = "".join(f"{d}={c}" for c, d in sorted(mapa.items(), key=lambda kv: kv[1]))
        if cifra is not None:
            avisos.append(f"números dos itens ofuscados; substituição de glifos decodificada ({cifra})")
    inicio_item = {i: (n, t) for i, n, t in numerados}

    itens: list[Item] = []
    blocos: list[Bloco] = []
    atual: Item | None = None
    bloco: Bloco | None = None
    secao: str | None = None
    estado = None  # ME: 'enunciado' | 'alt' | 'just'
    ultima_alt: str | None = None
    recentes: list[Bloco] = []

    def novo_bloco(l: Linha):
        nonlocal bloco
        bloco = Bloco(len(blocos) + 1, [l])
        blocos.append(bloco)
        recentes.append(bloco)

    for i, l in enumerate(linhas):
        if (blocos_lingua or lado_a_lado) and i in titulos_lingua:
            atual = None
            bloco = None
            recentes.clear()
            continue
        s = _secao(l)
        if s:
            secao = s
            atual = None
            bloco = None
            recentes.clear()
            continue
        if formato_me:
            m = _QUESTAO.match(l.texto)
            if m and cab_questao(l):
                atual = Item(int(m.group(1)), "DISC" if modalidade == "discursiva" else "ME", secao=secao,
                             numero_bruto=m.group(1), variante=rotulo_lingua(i, int(m.group(1))))
                if m.group(2):
                    atual.linhas.append(Linha(l.pagina, l.col, l.x0, l.y0, l.x1, l.y1, m.group(2), l.tamanho, l.origem))
                _vincula(atual, recentes)
                itens.append(atual)
                bloco = None
                estado, ultima_alt = "enunciado", None
                continue
            if atual is not None:
                if _JUST.match(l.texto):
                    estado = "just"
                    continue
                if estado == "just":
                    atual.justificativa.append(l)
                    ult = ultima_alt if atual.tipo == "ME" else None
                    if l.texto.rstrip().endswith("*/") and (ult is None or _ultima_just(atual) == ult):
                        atual, estado = None, None
                    continue
                ma = _ALT.match(l.texto)
                prox = "A" if ultima_alt is None else chr(ord(ultima_alt) + 1)
                if ma and ma.group(1) == prox and na_margem(l) and atual.tipo == "ME" and \
                        (prox != "A" or _proxima_alt(linhas, i, na_margem) == "B"):
                    ultima_alt = prox
                    atual.alternativas[prox] = [Linha(l.pagina, l.col, l.x0, l.y0, l.x1, l.y1, ma.group(2), l.tamanho, l.origem)]
                    estado = "alt"
                    continue
                if estado == "alt":
                    if not na_margem(l) and ultima_alt:
                        atual.alternativas[ultima_alt].append(l)
                        continue
                    if ultima_alt == "E":
                        atual = None
                    else:
                        atual.alternativas[ultima_alt].append(l)
                        continue
                else:
                    atual.linhas.append(l)
                    continue
            if bloco is None:
                novo_bloco(l)
            else:
                bloco.linhas.append(l)
            continue

        # ---------- formato C/E
        if i in inicio_item:
            n, tok = inicio_item[i]
            texto = l.texto[len(tok):].strip()
            atual = Item(n, "DISC" if modalidade == "discursiva" else "CE", secao=secao, numero_bruto=tok,
                         variante=rotulo_lingua(i, n))
            atual.linhas.append(Linha(l.pagina, l.col, l.x0, l.y0, l.x1, l.y1, texto, l.tamanho, l.origem))
            _vincula(atual, recentes)
            itens.append(atual)
            bloco = None
            continue
        if atual is not None and not na_margem(l) and not (bloco and bloco.linhas and bloco.linhas[-1] is l):
            if atual.justificativa or _JUST_CE.match(l.texto):
                atual.justificativa.append(l)      # "JUSTIFICATIVA - Certo. ..." (provas com justificativas)
            else:
                atual.linhas.append(l)
            continue
        atual = None
        if bloco is None:
            novo_bloco(l)
        else:
            bloco.linhas.append(l)

    for b in blocos:
        m = _FAIXA.search(b.texto)
        if m:
            a, z = int(m.group(1)), int(m.group(2))
            if a <= z:
                b.faixa = (a, z)
    # item -> texto-base: bloco cuja faixa cobre o item; senão o bloco mais recente
    for it in itens:
        cobrem = [b for b in it.blocos_anteriores if b.faixa and b.faixa[0] <= it.numero <= b.faixa[1]]
        cobrem += [b for b in blocos if b.faixa and b.faixa[0] <= it.numero <= b.faixa[1] and b not in cobrem]
        if cobrem:
            it.bloco = cobrem[0]
        elif it.blocos_anteriores:
            it.bloco = it.blocos_anteriores[-1]

    if modalidade == "discursiva" and not itens:
        corpo = [l for l in linhas]
        if corpo:
            it = Item(1, "DISC", list(corpo), secao=secao)
            itens = [it]
            blocos = []
            avisos.append("discursiva sem numeração: texto inteiro como questão 1")

    # "Questão N" sem nenhuma alternativa em toda a prova => questões discursivas
    if formato_me and itens and all(not it.alternativas for it in itens if it.tipo == "ME"):
        for it in itens:
            it.tipo = "DISC"
    tipos = {it.tipo for it in itens}
    tipo = tipos.pop() if len(tipos) == 1 else ("misto" if tipos else "vazio")
    if not formato_me and cands and len(numerados) < len(cands):
        descartados = len(cands) - len(numerados)
        if descartados:
            avisos.append(f"{descartados} linha(s) com número na margem fora da sequência de itens")
    return ResultadoProva(itens, blocos, tipo, cifra, avisos)


def _proxima_alt(linhas: list[Linha], i: int, na_margem) -> str | None:
    for l in linhas[i + 1:]:
        if _QUESTAO.match(l.texto) or _JUST.match(l.texto):
            return None
        m = _ALT.match(l.texto)
        if m and na_margem(l):
            return m.group(1)
    return None


def _ultima_just(it: Item) -> str | None:
    for l in reversed(it.justificativa):
        m = _JUST_ALT.match(l.texto)
        if m:
            return m.group(1)
    return None


def _vincula(it: Item, recentes: list[Bloco]) -> None:
    it.blocos_anteriores = list(recentes)


def _resolve_substituicao(cands: list[tuple[int, str, str]]) -> dict[str, str] | None:
    """Aprende a substituição glifo->dígito supondo itens consecutivos (s, s+1, ...) em ordem de leitura."""
    fontes = collections.Counter(f for _, t, f in cands if not _dig(t))
    fonte = fontes.most_common(1)[0][0] if fontes else None
    toks = [t for _, t, f in cands if f == fonte]
    if len(toks) < 3:
        return None
    melhor: tuple[int, dict[str, str]] | None = None
    for s in range(1, 301):
        mapa: dict[str, str] = {}
        usado: dict[str, str] = {}
        e, ok = s, 0
        for t in toks:
            for salto in range(3):                 # tolera até 2 itens não detectados
                alvo = str(e + salto)
                if len(t) != len(alvo):
                    continue
                novo = dict(mapa)
                nu = dict(usado)
                bom = True
                for ch, dg in zip(t, alvo):
                    if novo.get(ch, dg) != dg or nu.get(dg, ch) != ch:
                        bom = False
                        break
                    novo[ch] = dg
                    nu[dg] = ch
                if bom:
                    mapa, usado = novo, nu
                    ok += 1
                    e += salto + 1
                    break
        if melhor is None or ok > melhor[0]:
            melhor = (ok, mapa)
    if melhor and melhor[0] >= max(3, int(0.6 * len(toks))):
        return melhor[1]
    return None


def _cadeia(nums: list[tuple[int, int, str]], esperados: set[int] | None, salto_max: int = 3
            ) -> list[tuple[int, int, str]]:
    """Maior sequência crescente em ordem de leitura com saltos de 1 a `salto_max` (itens não detectados)."""
    if esperados:
        nums = [x for x in nums if x[1] in esperados] or nums
    n = len(nums)
    if not n:
        return []
    best = [1] * n
    prev: list[int | None] = [None] * n
    ult: dict[int, int] = {}          # número -> índice com melhor cadeia terminando nele
    for j, (_, v, _) in enumerate(nums):
        for d in range(1, salto_max + 1):
            k = ult.get(v - d)
            if k is not None and best[k] + 1 - (d - 1) * 0.01 > best[j]:
                best[j] = best[k] + 1
                prev[j] = k
                break
        if v not in ult or best[j] >= best[ult[v]]:
            ult[v] = j
    j = max(range(n), key=lambda x: best[x])
    out = []
    while j is not None:
        out.append(nums[j])
        j = prev[j]
    return out[::-1]
