"""Fase 5b — conteúdo programático dos editais de abertura ("OBJETOS DE AVALIAÇÃO") como guia da classificação.

1. ``ler_edital``: lê, do PDF do edital de abertura, as disciplinas de cada bloco/cargo/área com os seus tópicos.
   O resultado fica em ``edital_disciplina`` (cache por documento + versão do leitor).
2. ``Classificador``: para cada questão, as candidatas são as disciplinas do edital do próprio cargo (e área) e do
   mesmo grupo de bloco (básicos/gerais × específicos). A escolha compara o **assunto literal do comando** com o nome
   e os tópicos de cada candidata (TF-IDF, sem LLM):

   * ``edital_assunto`` — a 1ª candidata tem nota pelo menos ``RAZAO_MIN`` vezes a da 2ª;
   * ``edital_unica``   — o cargo/área tem uma única disciplina (ou só uma área) no edital;
   * ``area_prova``     — o edital não tem conteúdo para a prova (ex.: residências): a área declarada na própria prova
     ("PROVA OBJETIVA - ÁREA PROFISSIONAL: NUTRIÇÃO"), só para itens de conhecimentos específicos.

   Sem nenhuma dessas condições, nada é atribuído pelo edital.
"""
from __future__ import annotations

import json
import logging
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

from . import config
from .texto import norm

log = logging.getLogger(__name__)

VERSAO_LEITOR = 4
RAZAO_MIN = 1.5

UP = "A-ZÀ-ÖØ-Þ"
_ROMANOS = r"(?:I|II|III|IV|V|VI|VII|VIII|IX|X)"
_NAO_DISC = re.compile(r"^(?:REQUISITOS?|VANTAGENS|REMUNERA|ATRIBUI|DESCRI|JORNADA|VAGAS|CARGA|LOCAL|TOTAL|TAXA|"
                       r"PER[ÍI]ODO|DATA|ENDERE|OBSERVA|NOTA|ITEM|SUBITEM|CRONOGRAMA|ANEXO|PROVA|CAR[ÁA]TER|"
                       r"HABILIDADES|CONHECIMENTOS|CARGOS?\b|[ÁA]REA\b|ESPECIALIDADE|FORMA[ÇC][ÃA]O|PERFIL|"
                       r"INTERNET|FONTE|SITE|E-MAIL|SAC|TELEFONE)", re.I)


# ------------------------------------------------------------------------------------------------- leitura
def texto_pdf(caminho: str | Path) -> str:
    import pymupdf
    with pymupdf.open(caminho) as d:
        t = unicodedata.normalize("NFC", "\n".join(p.get_text() for p in d))   # acentos decompostos (EMAP)
    return re.sub(r"[  -​ ]", " ", t)                    # espaços não separáveis


def recorte(t: str) -> str:
    """Do último título "OBJETOS DE AVALIAÇÃO"/"CONTEÚDO PROGRAMÁTICO" seguido de disciplinas até o 1º "ANEXO"."""
    disc = re.compile(rf"\n[{UP}][{UP}0-9 ,()/–\-.ºª'’]{{3,140}}:\s*(?:{_ROMANOS}\s+[{UP}].*?:\s*)?1\.?\s", re.M)
    ini = None
    for m in re.finditer(r"OBJETOS\s+DE\s+AVALIA|CONTE[ÚU]DOS?\s+PROGRAM[ÁA]TICOS?", t):
        if disc.search(t[m.start():m.start() + 6000]):
            ini = m.start()
    if ini is None:
        m = disc.search(t)
        if not m:
            return ""
        ini = max(0, m.start() - 400)
    fim = re.search(r"\n\s*ANEXO\s+(?:I|[ÚU]NICO|1)\b", t[ini:])
    return t[ini:ini + fim.start()] if fim else t[ini:]


def _cargos(s: str) -> list[int] | None:
    """Números de cargo de um título ("CARGOS 2 A 14", "CARGOS 1, 3 E 5", "CARGO 7"); None = todos/indefinido."""
    if re.search(r"TODOS\s+OS\s+CARGOS|TODAS\s+AS\s+[ÁA]REAS|TODOS\s+OS\s+PERFIS", s):
        return None
    m = re.search(r"CARGOS?\s+((?:\d+\s*(?:,|E|A|AO|À|-|–)?\s*)+)", s)
    if not m:
        return None
    nums: list[int] = []
    partes = re.findall(r"\d+|A|AO|À|-|–", m.group(1))
    i = 0
    while i < len(partes):
        if partes[i].isdigit():
            if i + 2 < len(partes) and partes[i + 1] in ("A", "AO", "À", "-", "–") and partes[i + 2].isdigit():
                nums += list(range(int(partes[i]), int(partes[i + 2]) + 1))
                i += 3
                continue
            nums.append(int(partes[i]))
        i += 1
    return nums or None


def _bloco(s: str) -> str | None:
    for nome, rx in (("basicos", r"B[ÁA]SICOS"), ("gerais", r"GERAIS"), ("especificos", r"ESPEC[ÍI]FICOS"),
                     ("complementares", r"COMPLEMENTARES"), ("especializados", r"ESPECIALIZADOS")):
        if re.search(r"CONHECIMENTOS\s+" + rx, s):
            return nome
    return None


def nomes_cargos(t: str) -> dict[int, str]:
    """{número: nome} de "CARGO 1: ANALISTA ..." em qualquer parte do edital (quadro de vagas etc.)."""
    out: dict[int, str] = {}
    for m in re.finditer(rf"CARGO\s+(\d+)\s*[:–-]\s*([{UP}][{UP} ,/()–\-]{{5,160}})", t):
        out.setdefault(int(m.group(1)), re.sub(r"\s+", " ", m.group(2)).strip())
    return out


def nomes_areas(t: str) -> dict[tuple[int | None, int], str]:
    """{(cargo, área): curso} do requisito: "2.2.5 ÁREA 5 REQUISITO: diploma ... graduação ... em Engenharia Civil,"."""
    out: dict[tuple[int | None, int], str] = {}
    for m in re.finditer(r"[ÁA]REA\s+(\d+)\s*\n?\s*REQUISITOS?:\s*(.{0,400}?)(?:,\s*fornecido|\s+reconhecid|\.\s)", t, re.S):
        c = re.search(r"(?:gradua[çc][ãa]o|curso)[^,]*?\s(?:em|de)\s+([A-ZÀ-Ü][^,;]+?)(?:\s+ou\s+|,|;|$)",
                      re.sub(r"\s+", " ", m.group(2)))
        if not c:
            continue
        cargo = None
        for mc in re.finditer(r"CARGO\s+(\d+)\s*:", t[:m.start()]):
            cargo = int(mc.group(1))
        out.setdefault((cargo, int(m.group(1))), c.group(1).strip())
    return out


def _tok_nome(s: str) -> set[str]:
    return {w for w in re.findall(r"[A-Z]{4,}", norm(s)) if w not in {"CARGO", "CARGOS", "PARA", "FORMACAO", "AREA",
                                                                    "ESPECIALIDADE"}}


def _cargos_por_nome(s: str, nomes: dict[int, str]) -> list[int] | None:
    """Título sem número ("... PARA O CARGO DE ANALISTA DO SEGURO SOCIAL") → número pelo nome do cargo."""
    m = re.search(r"CARGOS?\s+(?:DE\s+)?([^\d].+)$", s)
    if not m or not nomes:
        return None
    q = _tok_nome(m.group(1))
    notas = sorted(((len(q & _tok_nome(n)) / max(1, len(q | _tok_nome(n))), k) for k, n in nomes.items()), reverse=True)
    if notas and notas[0][0] >= 0.5 and (len(notas) == 1 or notas[0][0] > notas[1][0]):
        return [notas[0][1]]
    return None


def parse(t: str) -> list[dict]:
    """Entradas {bloco, cargos, area, disciplina, tipo, topicos} do conteúdo programático.

    tipo 'disciplina' = título "DISCIPLINA: 1 ..."; 'area' = tópicos direto sob o cargo/área (sem disciplinas)."""
    nomes = nomes_cargos(t)
    s = recorte(t)
    s = re.sub(r"-\n(?=[a-zà-ü])", "", s)
    # disciplinas em romanos no meio da linha (ANA): "... III SISTEMAS HIDRÁULICOS DE SANEAMENTO: 1 ..." e nomes
    # quebrados ("I \nHIDROLOGIA: \n1") → cada nome numa linha própria, sem o numeral
    s = re.sub(rf"(?:(?<=\s)|^){_ROMANOS}\s+([{UP}][{UP}0-9 ,()/–\-\n]{{2,160}}?):\s*(?=\d)",
               lambda m: "\n" + re.sub(r"\s+", " ", m.group(1)).strip() + ": ", s, flags=re.M)
    out: list[dict] = []
    bloco = None
    cargos: list[int] | None = None
    area: int | None = None
    atual: dict | None = None
    pend_titulo = ""
    ultimas: list[str] = []

    def novo(disc, tipo, resto):
        nonlocal atual
        atual = {"bloco": bloco, "cargos": cargos, "area": area, "disciplina": disc, "tipo": tipo, "topicos": resto}
        out.append(atual)

    for l in (x.strip() for x in s.splitlines()):
        if not l or re.fullmatch(r"[\d/.\s]+", l):
            continue
        sem_num = re.sub(r"^\d+(?:\.\s?\d+)*\.?\s+", "", l)
        alto = sem_num == sem_num.upper() and re.search(rf"[{UP}]{{3}}", sem_num)
        if pend_titulo and alto and ":" not in sem_num.rstrip(":"):     # título quebrado em linhas
            pend_titulo += " " + sem_num
            if cargos is None:
                cargos = _cargos(pend_titulo) or _cargos_por_nome(pend_titulo, nomes)
            continue
        pend_titulo = ""
        if alto and re.match(r"CONHECIMENTOS\s+(?:B[ÁA]SICOS|GERAIS|ESPEC[ÍI]FICOS|COMPLEMENTARES|ESPECIALIZADOS)", sem_num):
            bloco = _bloco(sem_num)
            cargos = _cargos(sem_num) or _cargos_por_nome(sem_num, nomes)
            area = None
            atual = None
            ultimas.clear()
            if sem_num.rstrip().endswith(":") or re.search(r"(?:PARA|DO|DE)\s*$", sem_num):
                pend_titulo = sem_num
            continue
        if alto and re.match(r"CARGOS?\s+\d", sem_num):
            cargos = _cargos(sem_num)
            m = re.search(r"[ÁA]REA\s+(\d+)", sem_num)
            area = int(m.group(1)) if m else None
            atual = None
            ultimas.clear()
            if re.search(r"[ÁA]REA\s+\d+\s*:", sem_num) or re.search(r":\s*\S", sem_num):
                novo(sem_num, "area", "")
            continue
        if alto and re.match(r"[ÁA]REA\s+\d+", sem_num):
            area = int(re.match(r"[ÁA]REA\s+(\d+)", sem_num).group(1))
            ultimas.clear()
            novo(sem_num, "area", "")
            continue
        if atual is not None and atual["tipo"] == "area" and not atual["topicos"].strip() and alto and \
                ":" not in sem_num and not re.match(r"\d", l):
            # continuação do título do cargo/área ("CARGO 9: ANALISTA – ESPECIALIDADE:" / "PSICOLOGIA")
            atual["disciplina"] += " " + sem_num
            continue
        m = re.match(rf"^([{UP}][{UP}0-9 ,()/–\-.ºª'’&]{{2,160}}?)\s*:\s*((?:\d|{_ROMANOS}\s).*|)$", l)
        if m and m.group(1) == m.group(1).upper() and not _NAO_DISC.match(m.group(1)):
            nome = m.group(1).strip()
            # "NOÇÕES DE DIREITO" / "CONSTITUCIONAL: 1 ..." — linhas em maiúsculas logo antes são o começo do nome
            # (inclusive logo após um título, e com ":" dentro de parênteses quebrados: "LÍNGUA INGLESA (APENAS PARA
            # O CARGO 2: ..." / "... TECNOLOGIA DA INFORMAÇÃO): 1 ...")
            while ultimas:
                prev, nos_topicos = ultimas[-1]
                aberto = nome.count(")") > nome.count("(")
                # grupo com subtítulo: "NOÇÕES DE DIREITO CONSTITUCIONAL, PENAL E PROCESSUAL PENAL: NOÇÕES DE DIREITO"
                # / "CONSTITUCIONAL: 1 ..." → o nome é o que vem depois do último ":" da linha anterior
                cauda = prev.rsplit(":", 1)[1].strip() if ":" in prev and not aberto else ""
                if cauda and cauda == cauda.upper() and re.search(rf"[{UP}]{{3}}", cauda) and \
                        not cauda.endswith((".", ";")):
                    nome = cauda + " " + nome
                    ultimas.pop()
                    if nos_topicos and atual is not None:
                        atual["topicos"] = atual["topicos"][: -(len(prev) + 1)]
                    break
                if not (prev == prev.upper() and re.search(rf"[{UP}]{{2}}", prev) and not prev.endswith((".", ";"))
                        and (":" not in prev or aberto) and not re.match(r"(?:CONHECIMENTOS|CARGOS?\s+\d|[ÁA]REA\s+\d)", prev)):
                    break
                ultimas.pop()
                nome = prev + " " + nome
                if nos_topicos and atual is not None:
                    atual["topicos"] = atual["topicos"][: -(len(prev) + 1)]
            ultimas.clear()
            novo(nome, "disciplina", m.group(2))
            continue
        if atual is not None:
            atual["topicos"] += " " + l
            ultimas.append((l, True))
        else:
            ultimas.append((l, False))
    # área sem "DISCIPLINA:" (ABIN): as disciplinas são os tópicos de 1º nível em maiúsculas ("1 MACROECONOMIA. ...")
    final: list[dict] = []
    rx = re.compile(rf"(?:^|(?<=\s))(\d{{1,2}})\s+([{UP}][{UP}0-9 ,()/–\-]{{3,120}}?)\.(?=\s)")
    for e in out:
        ms = [m for m in rx.finditer(e["topicos"]) if not re.search(r"[a-zà-ü]", m.group(2))] if e["tipo"] == "area" else []
        nums = [int(m.group(1)) for m in ms]
        if len(ms) >= 2 and nums == sorted(nums) and nums[0] == 1:
            for k, m in enumerate(ms):
                fim = ms[k + 1].start() if k + 1 < len(ms) else len(e["topicos"])
                final.append({**e, "disciplina": m.group(2).strip(), "tipo": "disciplina",
                              "topicos": e["topicos"][m.end():fim]})
        else:
            final.append(e)
    areas = nomes_areas(t)
    for e in final:
        e["disciplina"] = re.sub(r"\s+", " ", re.sub(r"^ESPECIALIDADE\s+\d+\s+", "", e["disciplina"])).strip()
        if e["tipo"] == "area" and re.fullmatch(r"[ÁA]REA\s+\d+", e["disciplina"]) and e["area"] is not None:
            for c in (e["cargos"] or [None]):          # área só com número: nome do curso exigido no requisito
                nome = areas.get((c, e["area"]))
                if nome:
                    e["disciplina"] = f"{e['disciplina']} – {nome}"
                    break
    # sem tópicos (só título), ou "área" cujo texto é só a continuação de um título (sem tópico numerado)
    return [e for e in final if len(e["topicos"].strip()) > 20
            and (e["tipo"] != "area" or re.search(r"(?:^|\s)1\.?\s+\S", e["topicos"]))]


def topicos(texto: str) -> list[str]:
    """Divide "1 X. 1.1 Y. 2 Z." em tópicos."""
    partes = re.split(r"(?:(?<=\.)|(?<=;)|^)\s*(\d+(?:\.\d+)*)\.?\s+(?=[A-ZÀ-Üa-zà-ü])", " " + texto)
    out = [f"{partes[i]} {partes[i + 1].strip(' .;')}" for i in range(1, len(partes) - 1, 2) if partes[i + 1].strip(" .;")]
    return out or [texto.strip()]


def rotulo_area(s: str | None) -> str | None:
    """"PROVA OBJETIVA - ÁREA PROFISSIONAL: NUTRIÇÃO" → "NUTRIÇÃO"; "CARGO 4: ... – ÁREA 3: INFORMÁTICA FORENSE" →
    "INFORMÁTICA FORENSE"; "ÁREA 5 – Engenharia Civil" → "Engenharia Civil"."""
    if not s:
        return None
    ms = re.findall(r"(?:[ÁA]REA(?:\s+PROFISSIONAL|\s+DE\s+FORMA[ÇC][ÃA]O)?|ESPECIALIDADE|PROGRAMA)\s*\d*\s*[:–-]\s*"
                    r"([^:–|]+?)\s*(?=$|[–|])", s, re.I)
    return ms[-1].strip() if ms else None


_GENERICOS = re.compile(r"^(?:ADMINISTRATIV|JUDICI[ÁA]RI|APOIO|GERAL|GERAIS|N[ÍI]VEL|T[ÉE]CNIC[OA]\b|OPERACIONAL|"
                        r"ESPECIALIZAD|FIM|MEIO|ATIVIDADE|SEM ESPECIALIDADE|QUALQUER|TODAS|[IVX]+$|\d)", re.I)


def rotulo_generico(s: str) -> bool:
    """Rótulos de área que não são área de conhecimento ("ADMINISTRATIVA", "JUDICIÁRIA", "APOIO ESPECIALIZADO")."""
    return bool(_GENERICOS.match(norm(s)))


# ------------------------------------------------------------------------------------------------- cache no banco
def edital_do_concurso(con, concurso_id: int):
    """O edital de abertura em PDF baixado: o 'atualizado conforme retificações', senão o publicado por último
    (uma republicação pode renumerar os cargos, e as provas seguem a numeração final)."""
    return con.execute("""SELECT * FROM documento WHERE concurso_id=? AND tipo='edital_abertura' AND acessibilidade=0
                          AND lower(COALESCE(extensao,''))='pdf' AND COALESCE(versao,'')<>'sem_efeito'
                          AND arquivo_local IS NOT NULL
                          ORDER BY (COALESCE(versao,'')='atualizado') DESC, COALESCE(data_publicacao,'') DESC, id DESC
                          LIMIT 1""", (concurso_id,)).fetchone()


def ler_edital(con, concurso_id: int) -> list[dict] | None:
    """Disciplinas do edital do concurso (do cache, ou lidas do PDF). None = não há edital baixado."""
    from . import db
    doc = edital_do_concurso(con, concurso_id)
    if doc is None:
        return None
    cache = con.execute("SELECT * FROM edital_disciplina WHERE documento_id=? AND versao_leitor=? ORDER BY ordem",
                        (doc["id"], VERSAO_LEITOR)).fetchall()
    if cache:
        return [dict(r) | {"cargos": json.loads(r["cargos"]) if r["cargos"] else None}
                for r in cache if r["tipo"] != "vazio"]
    caminho = Path(doc["arquivo_local"])
    caminho = caminho if caminho.is_absolute() else config.ROOT / caminho
    if not caminho.exists():
        return None
    try:
        ents = parse(texto_pdf(caminho))
    except Exception as e:  # noqa: BLE001
        db.pendencia(con, "disciplina", f"edital ilegível: {type(e).__name__}: {str(e)[:150]}", concurso_id, doc["id"])
        return []
    con.execute("DELETE FROM edital_disciplina WHERE documento_id=?", (doc["id"],))
    linhas = [(doc["id"], concurso_id, k, e["bloco"], json.dumps(e["cargos"]) if e["cargos"] else None, e["area"],
               e["disciplina"], e["tipo"], e["topicos"].strip(), VERSAO_LEITOR) for k, e in enumerate(ents)]
    if not linhas:      # marcador: edital lido, sem conteúdo programático (não relê a cada execução)
        linhas = [(doc["id"], concurso_id, 0, None, None, None, "", "vazio", "", VERSAO_LEITOR)]
        db.pendencia(con, "disciplina", "edital de abertura sem conteúdo programático legível", concurso_id, doc["id"])
    con.executemany("""INSERT INTO edital_disciplina(documento_id, concurso_id, ordem, bloco, cargos, area, nome, tipo,
                       topicos, versao_leitor) VALUES (?,?,?,?,?,?,?,?,?,?)""", linhas)
    return [{"bloco": e["bloco"], "cargos": e["cargos"], "area": e["area"], "nome": e["disciplina"], "tipo": e["tipo"],
             "topicos": e["topicos"]} for e in ents]


# ------------------------------------------------------------------------------------------------- classificação
_STOP = set("""DE DA DO DAS DOS EM NO NA NOS NAS COM POR PARA QUE OS AS UM UMA SEUS SUAS SEU SUA AO AOS ENTRE SOBRE
SEM SOB COMO MAIS MENOS OU NAO SAO SER TEM QUAL QUAIS ESSE ESSA ESTE ESTA ITEM ITENS JULGUE SEGUIR SUBSEQUENTES
SEGUINTES OPCAO CORRETA ASSINALE ACERCA RESPEITO RELACAO CONSIDERANDO CONCEITO CONCEITOS NOCOES NOCAO ASPECTOS LEI
DECRETO ARTIGO ART PARTE GERAL TIPOS FORMAS CARACTERISTICAS PRINCIPAIS BASICOS BASICAS FUNDAMENTOS APLICACAO
ALTERACOES DISPOSTO NORMAS ACORDO CASO SITUACAO HIPOTETICA TEXTO""".split())
_GRUPO_BAS = ("basicos", "gerais")
_GRUPO_ESP = ("especificos", "especializados", "complementares")


def _toks(s: str | None) -> list[str]:
    return [w[:6] for w in re.findall(r"[A-Z]{3,}", norm(s)) if w not in _STOP]


def cargo_area(cargo: str | None) -> tuple[set[int], int | None]:
    c = norm(cargo)
    m = re.search(r"AREA\s+(\d+)", c)
    return {int(n) for n in re.findall(r"CARGOS?\s+(\d+)", c)}, (int(m.group(1)) if m else None)


def suspeita(texto: str) -> bool:
    """Numeração de 1º nível que recomeça ("1 ... 6 ... 2 ... 4 ...") — a disciplina engoliu outras cujos títulos não
    foram reconhecidos, e os tópicos dela não são confiáveis para decidir."""
    nums = [int(n) for n in re.findall(r"(?:^|[.;:]\s)(\d{1,2})\.?\s+[A-ZÀ-Ü]", " " + texto)]
    return any(b < a for a, b in zip(nums, nums[1:]))


class Classificador:
    """Disciplinas do edital de um concurso, vetorizadas uma vez; ``classificar`` decide por questão."""

    def __init__(self, entradas: list[dict]):
        self.e = [x for x in entradas if x["tipo"] == "disciplina" or rotulo_area(x["nome"])]
        for x in self.e:
            x["rotulo"] = (rotulo_area(x["nome"]) or x["nome"]) if x["tipo"] == "area" else x["nome"]
            x["suspeita"] = suspeita(x["topicos"]) if x["tipo"] == "disciplina" else False
        docs = [Counter(_toks(x["rotulo"]) * 3 + _toks(x["topicos"])) for x in self.e]
        df = Counter(t for d in docs for t in set(d))
        n = max(1, len(docs))
        self.idf = {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}
        self.vd = [self._vet(d) for d in docs]
        # cada tópico também é um vetor: o assunto do comando costuma repetir um tópico quase literalmente
        self.vt = [[self._vet(Counter(_toks(tp))) for tp in topicos(x["topicos"])] for x in self.e]

    def _vet(self, c: Counter) -> dict:
        v = {t: (1 + math.log(f)) * self.idf.get(t, 0) for t, f in c.items() if self.idf.get(t, 0) > 0}
        nn = math.sqrt(sum(x * x for x in v.values())) or 1
        return {t: x / nn for t, x in v.items()}

    def candidatas(self, cargos: set[int], area: int | None, bloco: str | None) -> list[int]:
        cand = [i for i, x in enumerate(self.e)
                if (x["cargos"] is None or not cargos or set(x["cargos"]) & cargos)
                and (x["area"] is None or area is None or x["area"] == area)]
        grupo = "esp" if bloco in _GRUPO_ESP else "bas" if bloco in _GRUPO_BAS else None
        if grupo:       # só o mesmo grupo de bloco (sem recair no outro: área sem disciplinas lidas → básicas)
            cand = [i for i in cand if self.e[i]["bloco"] is None or (self.e[i]["bloco"] in _GRUPO_BAS) == (grupo == "bas")]
        unicas: dict[str, int] = {}
        for i in cand:
            unicas.setdefault(norm(self.e[i]["rotulo"]), i)
        return list(unicas.values())

    def classificar(self, assunto: str | None, cargos: set[int], area: int | None,
                    bloco: str | None) -> tuple[str | None, str | None, float | None]:
        """(nome no edital, fonte, razão 1ª/2ª) ou (None, motivo, None)."""
        cand = self.candidatas(cargos, area, bloco)
        if not cand:
            return None, "sem_candidata", None
        if not cargos and area is None and \
                len({json.dumps(self.e[i]["cargos"]) for i in cand if self.e[i]["cargos"] is not None}) > 1:
            # prova sem cargo/área identificados e candidatas de cargos diferentes: escolher seria chute
            return None, "cargo_indefinido", None
        if len(cand) == 1:
            return self.e[cand[0]]["rotulo"], "edital_unica", None
        if not assunto:
            return None, "sem_assunto", None
        vq = self._vet(Counter(_toks(assunto)))

        def nota(i):
            geral = sum(vq.get(t, 0) * x for t, x in self.vd[i].items())
            top = max((sum(vq.get(t, 0) * x for t, x in v.items()) for v in self.vt[i]), default=0.0)
            return 0.5 * geral + 0.5 * top
        notas = sorted(((nota(i), i) for i in cand), reverse=True)
        s1, s2 = notas[0][0], notas[1][0]
        if s1 <= 0:
            return None, "sem_semelhanca", 0.0
        razao = s1 / s2 if s2 > 0 else float("inf")
        if razao < RAZAO_MIN:
            return None, "abaixo_do_limiar", razao
        if self.e[notas[0][1]]["suspeita"]:
            return None, "edital_suspeito", razao
        return self.e[notas[0][1]]["rotulo"], "edital_assunto", razao
