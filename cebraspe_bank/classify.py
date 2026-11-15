"""Classificação de documentos pelo nome do arquivo e pelo texto do link (descricaoArquivo).

Casos ambíguos recebem revisar=1 e um motivo; nunca se inventa o tipo.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .texto import limpa, norm

TIPOS_CONTEUDO = {
    "prova", "prova_com_gabarito_preliminar", "prova_com_gabarito_definitivo",
    "gabarito_preliminar", "gabarito_definitivo", "justificativa", "padrao_resposta",
}

_ACESS = re.compile(
    r"ADAPTAD|SUPER ?AMPLIAD|\bSUPER\b|\bLEDOR\b|BRAILLE|V ?LIBRAS|\bLIBRAS\b|\bTXT\b|AMPLIADA|TRANSCRITOR"
)
_EXT_MIDIA = {"html", "htm", "mp4", "mp3", "png", "w", "e", "undefined"}
_EDITALISH = re.compile(
    r"\bRESULTAD|\bCONVOCA|\bLOCA(L|IS)\b|\bEDITAL\b|\bED \d|\bRELACAO\b|\bCONSULTA\b|\bRECURSO|\bCRONOGRAMA"
    r"|\bAVISO\b|\bCOMUNICADO\b|\bINSTRU(C|CA)O|\bMANUAL\b|\bTITULOS\b|\bHETEROIDENTIF|\bBIOPSICO|\bPERICIA"
    r"|\bINSCRI|\bISENCAO\b|\bDESEMPENHO\b|\bNOTAS?\b|\bBANCAS?\b|MOVIMENTA|DEMONSTRATIVO|COMPOSICAO|RELATORIO"
)
_PADRAO = re.compile(r"PADR(A?O|AO|  O|O)\b.*RESPOSTA|PADRAORESPOSTA|PADR O DE RESPOSTA|\bPADRAO\b|\bPADR  O\b|\bPADRO\b")
_PROVA_DESC = re.compile(
    r"^(CADERNO|PROVAS?\b|CONHECIMENTOS\b|QUESTOES? (DISCURSIVAS?|OBJETIVAS?)|[A-Z]+ FASE [-|] PROVA\b)"
    r"|\bPROVAS? (OBJETIVAS?|DISCURSIVAS?|DE CONHECIMENTOS|ESCRITAS?|SUBJETIVAS?)\b|\bCADERNO DE PROVAS?\b"
)
_PROVA_FORTE = re.compile(
    r"^(CADERNO DE PROVAS?|PROVAS? (OBJETIVAS?|DISCURSIVAS?|ESCRITAS?|SUBJETIVAS?|TE.{0,2}RICAS?)|CONHECIMENTOS (BASICOS|GERAIS|ESPECIFICOS|COMPLEMENTARES))\b"
)
_NAO_PROVA = re.compile(r"PROVA ORAL|\bORAL\b|DIGITACAO|APTIDAO FISICA|TAF\b|PRATICA DE (DIRECAO|CONDUCAO)"
                        r"|^CAPA\b|\bPROVAS? - CAPA\b|- CAPA$")
# provas escritas de resposta livre que não dizem "discursiva": prática (peça, parecer, sentença), situação-problema,
# caso da prova de tribuna (publicado com padrão de resposta)
_DISC_EXTRA = re.compile(r"PROVA PRATICA|PRATICA DE SENTENCA|HABILIDADES CLINICAS|SITUACAO PROBLEMA|\bSENTENCA\b"
                         r"|\bPECA (JUDICIAL|PROCESSUAL|PRATICA)\b|\bTRIBUNA\b|CASO HIPOTETICO")
_PROVA_NOME = re.compile(r"^(MATRIZ )?\d{3} ?[A-Z0-9]+( [A-Z0-9]+)* (CB\d+|CG\d+|CE\d+|DISC|\d{3})( \d+)*( CADERNO [A-Z]+)?$")

_PREFIXOS = re.compile(r"^(GAB(ARITO)?_?(DEFINITIVO|PRELIMINAR)_|MATRIZ_|XX)+", re.I)
_SUFIXOS = re.compile(
    r"(_+(COM[ _]JUSTIFICATIVAS.*|CADERNO_\w+|LEDOR|SUPER\w*|ADAPTADA|TXT|ATUALIZADO|ATT|OK|VF|MATRIZ|PAG_?\d+|V_?\d+))+$", re.I
)
_CODIGO_OK = re.compile(r"^\d{3}_?[A-Z0-9]+(_[A-Z0-9]+)*$")
_BLOCO = re.compile(r"_(CB\d+|CG\d+|CE\d+|DISC|\d{3})(?=_|$)")
_BLOCO_DISC = re.compile(r"_(\d{3})_DISC$|_DISC_(\d+)")
_CADERNO = re.compile(r"\bCADERNO\s+(?!DE\b)([A-Z\u00C0-\u00DC]{3,})\b", re.I)
_CADERNO_NOME = re.compile(r"_CADERNO_([A-Z]+)", re.I)
_CARGO = re.compile(r"\b(CARGOS?\s*(?:DE\s+)?(?:N[IÍ]VEL\s+\w+|\d.*|[A-ZÀ-Ü].*))", re.I)


@dataclass
class Classificacao:
    tipo: str
    modalidade: str | None = None
    acessibilidade: bool = False
    versao: str | None = None
    cargo: str | None = None
    caderno: str | None = None
    codigo_prova: str | None = None
    bloco: str | None = None
    revisar: bool = False
    motivos: list[str] = field(default_factory=list)


def codigo_prova(nome_arquivo: str) -> tuple[str | None, str | None]:
    base = re.sub(r"\.[A-Za-z0-9]{2,5}$", "", nome_arquivo.strip())
    if re.fullmatch(r"[0-9A-Fa-f]{64}", base):
        return None, None
    b = _PREFIXOS.sub("", base)
    b = _SUFIXOS.sub("", b)
    b = re.sub(r"\s+", "_", b).upper()
    if not _CODIGO_OK.match(b) or "_" not in b:
        return None, None
    m = _BLOCO_DISC.search(b)
    if m:
        return b, "DISC"
    ms = _BLOCO.findall(b[b.find("_"):])
    return b, (ms[-1] if ms else None)


def _cargo(desc: str) -> str | None:
    d = limpa(desc)
    m = _CARGO.search(d)
    if not m:
        return None
    c = m.group(1)
    c = re.split(r"\s+[-–]\s+(?=(ADAPTAD|SUPER|LEDOR|BRAILLE|TXT|\(?ATUALIZ|\(?SEM EFEITO))", c, flags=re.I)[0]
    c = re.split(r":\s*CADERNO\b", c, flags=re.I)[0]
    c = re.sub(r"\s*\((ATUALIZADO|SEM EFEITO)\)\s*$", "", c, flags=re.I)
    return c.strip(" -–:") or None


def classificar(nome_arquivo: str, descricao: str | None, extensao: str | None = None) -> Classificacao:
    n = norm(re.sub(r"\.[A-Za-z0-9]{2,5}$", "", nome_arquivo.strip()))
    d = norm(descricao)
    nd = f"{d} | {n}"
    ext = (extensao or "").lower().lstrip("_.")
    if not ext:
        m = re.search(r"\.([A-Za-z0-9]{1,5})$", nome_arquivo)
        ext = m.group(1).lower() if m else ""

    c = Classificacao(tipo="outro")
    if _ACESS.search(nd) or ext in _EXT_MIDIA:
        c.acessibilidade = True
    if "SEM EFEITO" in nd:
        c.versao = "sem_efeito"
    elif re.search(r"ATUALIZAD|\bATT\b", nd):
        c.versao = "atualizado"

    tem_gab = bool(re.search(r"\bGAB(ARITOS?)?\b", nd))
    forte = bool(_PROVA_FORTE.match(d))
    tem_prova = forte or bool(_PROVA_DESC.search(d)) or bool(re.search(r"\bPROVAS? (OBJETIVA|DISCURSIVA)", d))
    prelim = "PRELIMINAR" in nd and "INSCRICAO PRELIMINAR" not in nd
    defin = "DEFINITIV" in nd and not re.search(r"TEXTO DEFINITIVO", nd)
    justif = "JUSTIFICATIVA" in nd

    if re.match(r"^PROVAS?\b.*\bE PADR(A?O|OES)\b.*RESPOSTA", d) and not _NAO_PROVA.search(d):
        c.tipo = "prova_com_gabarito_definitivo" if "PRELIMINAR" not in d and "PROVISORIO" not in d \
            else "prova_com_gabarito_preliminar"
        c.modalidade = "discursiva"
    elif _NAO_PROVA.search(d) and not justif:
        c.tipo = "outro"
        c.motivos.append("prova oral/prática/física: fora do escopo")
    elif re.match(r"^JUSTIFICATIVAS?\b", d) and re.search(r"ALTERA|ANULA|GABARITO", d):
        c.tipo = "justificativa"
    elif justif and tem_prova and tem_gab:
        c.tipo = "prova_com_gabarito_definitivo" if defin and not prelim else "prova_com_gabarito_preliminar"
    elif justif and (tem_gab or re.search(r"ALTERA|ANULA", nd)):
        c.tipo = "justificativa"
    elif _PADRAO.search(nd) and re.search(r"RESPOSTA|PADRAORESPOSTA|\bPDR\b", nd) and \
            not re.match(r"^(EDITAL|COMUNICADO|AVISO|RESPOSTAS? AOS? RECURSOS?|RECURSO)", d) and "RECURSO" not in d:
        c.tipo = "padrao_resposta"
        c.modalidade = "discursiva"
    elif re.match(r"^(PROVAS?|CADERNO)\b.*\bE GABARITOS?\b", d) and not _EDITALISH.search(d):
        if prelim == defin:
            c.tipo = "prova_com_gabarito_definitivo" if defin else "prova_com_gabarito_preliminar"
            if prelim == defin:
                c.revisar = True
                c.motivos.append("prova+gabarito sem fase clara (preliminar/definitivo)")
        else:
            c.tipo = "prova_com_gabarito_definitivo" if defin else "prova_com_gabarito_preliminar"
    elif tem_gab and not _EDITALISH.search(d.replace("GABARITO", "")) or re.match(r"^GAB ", n):
        if prelim and not defin:
            c.tipo = "gabarito_preliminar"
        elif defin and not prelim:
            c.tipo = "gabarito_definitivo"
        else:
            c.tipo = "gabarito_definitivo" if defin else "gabarito_preliminar"
            c.revisar = True
            c.motivos.append("gabarito sem fase clara (preliminar/definitivo)")
    elif tem_prova and (forte or not _EDITALISH.search(d)):
        c.tipo = "prova"
    elif _PROVA_NOME.match(n) and not _EDITALISH.search(d):
        c.tipo = "prova"
        c.revisar = True
        c.motivos.append("prova inferida só pelo nome do arquivo")
    elif re.search(r"\bEDITAL\b|^ED ?\d|^EDITAL|^COMUNICADO N", nd) or re.match(r"^ED ", n):
        abertura = (re.match(r"^(PORTARIA CONJUNTA E )?(EDITAL|COMUNICADO)\s+N(O|\.|°|º)?\W{0,3}\s*\d+\s*(/\s*\d{2,4}\s*)?[-:]?\s*(DE\s+)?ABERTURA\b", d)
                    or re.match(r"^EDITAL DE ABERTURA\b", d)) and not re.search(r"REABERTURA|PRAZO|IMPUGNA", d)
        c.tipo = "edital_abertura" if abertura else "edital"
    else:
        c.tipo = "outro"

    if c.tipo in TIPOS_CONTEUDO and c.modalidade is None:
        if re.search(r"DISCURSIVA|REDACAO|\bDISC\b|SUBJETIVA|PROVA ESCRITA|PECA PROCESSUAL|PARECER|ESTUDO DE CASO", nd) \
                or (_DISC_EXTRA.search(nd) and c.tipo.startswith(("prova", "padrao"))):
            c.modalidade = "discursiva"
        elif re.search(r"OBJETIVA|CONHECIMENTOS|\bCB\d|\bCG\d", nd) or c.tipo.startswith("gabarito"):
            c.modalidade = "objetiva"

    c.codigo_prova, c.bloco = codigo_prova(nome_arquivo)
    if c.modalidade == "discursiva" and c.bloco and c.bloco != "DISC" and "DISC" in (c.codigo_prova or ""):
        c.bloco = "DISC"
    c.cargo = _cargo(descricao or "")
    m = _CADERNO.search(limpa(descricao)) or _CADERNO_NOME.search(nome_arquivo)
    if m:
        c.caderno = m.group(1).upper()
    if c.tipo in TIPOS_CONTEUDO and c.codigo_prova is None and not c.acessibilidade:
        c.motivos.append("sem código de prova no nome (vínculo depende do texto do PDF)")
    return c
