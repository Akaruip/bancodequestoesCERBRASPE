"""Fase 5 — bloco, assunto e disciplina das questões, sem LLM.

Três informações, cada uma com a sua fonte:

* ``bloco``: o bloco da prova onde a questão está ("CONHECIMENTOS BÁSICOS" → ``basicos``), normalizado a partir de
  ``questao.secao`` (título lido no PDF).
* ``assunto``: trecho **literal** do comando que introduz a questão ("Acerca de atos administrativos, julgue os
  itens…" → ``atos administrativos``). Trechos que só apontam para o contexto ("a situação hipotética precedente",
  "essas informações") são descartados. Quando o comando não tem trecho temático, o assunto fica NULL.
* ``disciplina``: em ordem de precedência,
  1. ``variante`` — item de opção de língua estrangeira (``questao.variante``);
  2. ``titulo_pdf`` — o título de bloco lido no PDF já é o nome de uma disciplina ("LÍNGUA PORTUGUESA");
  3. ``regra_assunto`` — o assunto literal casa com uma regra da tabela ``REGRAS`` (palavras-chave revisáveis).
  Sem nenhuma dessas fontes a disciplina fica NULL: nada é estimado por posição, cargo ou vizinhança.

A tabela de regras é deliberadamente conservadora; uma regra que acerta pouco deve ser removida, não afrouxada.
"""
from __future__ import annotations

import logging
import re

from .texto import limpa, norm

log = logging.getLogger(__name__)

VERSAO = 1

# ----------------------------------------------------------------------------------------------- bloco
_BLOCOS = [
    ("discursiva", r"DISCURSIV|REDACAO|PECA PROCESSUAL|SENTENCA|PARECER|ESCRITA P\d"),
    ("basicos", r"CONHECIMENTOS BASICOS|BLOCO I\b(?! ?I)"),
    ("gerais", r"CONHECIMENTOS GERAIS"),
    ("complementares", r"CONHECIMENTOS COMPLEMENTARES"),
    ("especializados", r"CONHECIMENTOS ESPECIALIZADOS"),
    ("especificos", r"CONHECIMENTOS ESPECIFICOS|BLOCO II|BLOCO III|CONHECIMENTOS II"),
    ("objetiva", r"PROVA|PARTE|FASE|BLOCO"),
]


def bloco(secao: str | None, tipo: str | None = None) -> str | None:
    """Bloco normalizado a partir do título de seção lido no PDF. Sem título → NULL (DISC → 'discursiva')."""
    s = norm(secao)
    for nome, rx in _BLOCOS:
        if s and re.search(rx, s):
            return nome
    if tipo == "DISC":
        return "discursiva"
    return None


# --------------------------------------------------------------------------------------------- assunto
# conectivos que introduzem o tema de um comando (texto normal, com acentos; casamento sem distinção de caixa)
_CONECT = (r"acerca\s+d[eoa]s?|a\s+respeito\s+d[eoa]s?|com\s+rela[çc][ãa]o\s+(?:a|à|ao|às|aos)|"
           r"em\s+rela[çc][ãa]o\s+(?:a|à|ao|às|aos)|no\s+que\s+(?:se\s+refere|concerne|diz\s+respeito|tange)\s+(?:a|à|ao|às|aos)|"
           r"quanto\s+(?:a|à|ao|às|aos)|relativamente\s+(?:a|à|ao|às|aos)|no\s+tocante\s+(?:a|à|ao|às|aos)|"
           r"com\s+refer[êe]ncia\s+(?:a|à|ao|às|aos)|sobre\s+(?:o|a|os|as)?|"
           r"(?:relativ|referent|concernent|pertinent|atinent|alusiv)[oae]s?\s+(?:a|à|ao|às|aos)|"
           r"com\s+base\s+n[oa]s?|de\s+acordo\s+com\s+(?:o|a|os|as)?|segundo\s+(?:o|a|os|as)|conforme\s+(?:o|a|os|as)?|"
           r"[àa]\s+luz\s+d[oa]s?|tendo\s+como\s+refer[êe]ncia\s+(?:o|a|os|as)?|considerando\s+(?:o|a|os|as)?|"
           r"tendo\s+em\s+vista\s+(?:o|a|os|as)?|nos\s+termos\s+d[oa]s?|em\s+conformidade\s+com\s+(?:o|a|os|as)?|"
           r"no\s+[âa]mbito\s+d[oa]s?|no\s+contexto\s+d[oa]s?|que\s+se\s+referem\s+(?:a|à|ao|às|aos)|"
           r"que\s+tratam\s+d[eoa]s?|que\s+versam\s+sobre|em\s+torno\s+d[eoa]s?")
_ACAO = r"julgue|assinale|judge|juzgue|indique|escolha"
# o tema vai do conectivo até a vírgula/ponto que o encerra
_RX_TEMA = re.compile(rf"(?:^|[\s,;(])(?:{_CONECT})\s+(.{{3,220}}?)\s*(?=[,.;:]\s|[,.;:]?$|,\s*(?:{_ACAO}))", re.I)
# trechos que só apontam para o contexto: não são assunto
_DEITICO = re.compile(
    r"^(?:(?:o|a|os|as|esse|essa|esses|essas|este|esta|estes|estas|tal|tais|aquel[ea]s?|referid[oa]s?|mencionad[oa]s?|"
    r"seguintes?|dess[ea]s?|dest[ea]s?|d[oa]s?|n[oa]s?|ao|aos|à|às)\s+)*"
    r"(?:texto|textos|trecho|fragmento|situa[çc][ãa]o|situa[çc][õo]es|caso|casos|cen[áa]rio|informa[çc][õo]es|dados|"
    r"figura|figuras|imagem|imagens|tabela|tabelas|quadro|quadros|gr[áa]fico|gr[áa]ficos|esquema|diagrama|c[óo]digo|"
    r"algoritmo|programa|script|trecho|hip[óo]tese|exemplo|planilha|janela|tela|modelo|circuito|mapa|f[óo]rmula|"
    r"equa[çc][ãa]o|express[ãa]o|sistema|fun[çc][ãa]o|conjunto|sequ[êe]ncia|proposi[çc][ãa]o|proposi[çc][õo]es|"
    r"argumento|afirma[çc][ãa]o|afirma[çc][õo]es|relato|not[íi]cia|reportagem|fato|fatos|ideias|poema|letra|"
    r"enunciado|resultado|resultados|consulta|comando|valores|medidas|par[âa]metros|instru[çc][õo]es|it(?:em|ens)|"
    r"assertivas?|declara[çc][ãa]o|documento|registro|cita[çc][ãa]o|of[íi]cio|of[íi]cios|assunto|tema|tem[áa]tica|"
    r"conte[úu]do|dispositivo)\b"
    r"(?:[^,]*?\b(?:precedentes?|anterior(?:es)?|acima|apresentad[oa]s?|hipot[ée]tic[oa]s?|mostrad[oa]s?|"
    r"descrit[oa]s?|ilustrad[oa]s?|dess[ea]s?|dest[ea]s?|ness[ea]s?|nest[ea]s?|considerad[oa]s?|exibid[oa]s?|a seguir|abaixo|em quest[ãa]o|"
    r"[A-Z]*\d+[A-Z]+\d*\w*|(?-i:[A-Z]))\b[^,]*)?$"
    # "os múltiplos aspectos a ele relacionados", "esse caso clínico"
    r"|^(?:o|a|os|as|aos|às)?\s*(?:m[úu]ltiplos|v[áa]rios|diversos|diferentes)?\s*aspectos(?:\s+diversos)?\s+a\s+el[ea]s?\s+relacionad"
    r"|^(?:o|a)?\s*caso\s+cl[íi]nico", re.I)
_SO_REFERENCIA = re.compile(r"^(?:n?ess[ea]s?|n?est[ea]s?|tais?|tal|aquel[ea]s?)\s+(?:[\w-]+\s*){1,3}$|^(?:o|a)\s+exposto$|^(?:o|a)\s+que\s+se\s+segue", re.I)


def _frase_comando(texto: str | None, acao: str = _ACAO) -> str | None:
    """A frase que contém a ação ("julgue", "assinale"...), ou None."""
    if not texto:
        return None
    t = limpa(texto)
    frases = re.split(r"(?<=[.?!])\s+(?=[A-ZÀ-Ú])", t)
    for f in reversed(frases):
        if re.search(rf"\b(?:{acao})\b", f, re.I):
            return f.strip()
    return None


def _limpa_tema(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip(" ,;:.–-")
    t = re.sub(r",?\s*(?:julgue|assinale|judge|juzgue)\b.*$", "", t, flags=re.I).strip(" ,;:.")
    return t


# "considerando as ideias, as propriedades linguísticas e o vocabulário do texto precedente": o conectivo pega só
# "as ideias"; o trecho literal até "texto" identifica a análise do texto (língua portuguesa)
_RX_LING = re.compile(r"(?:ideias|aspectos\s+(?:lingu[íi]sticos|gramaticais|discursivos|sem[âa]nticos|sint[áa]ticos|"
                      r"textuais)|propriedades\s+lingu[íi]sticas|estruturas\s+lingu[íi]sticas|vocabul[áa]rio)"
                      r"[^.;]{0,100}?\btexto\b", re.I)
# comandos escritos em inglês/espanhol (o próprio idioma do comando identifica a disciplina)
_RX_INGLES = re.compile(r"\bjudge\b|\bthe\s+following\s+items?\b|\bthe\s+text\b", re.I)
_RX_ESPANHOL = re.compile(r"\bjuzgue\b|\bdel\s+texto\b|\blos\s+(?:siguientes\s+)?[íi]tems\b", re.I)


def temas(frase: str | None) -> list[str]:
    """Trechos temáticos literais de uma frase de comando, sem os que só apontam para o contexto."""
    if not frase:
        return []
    out: list[str] = []
    for m in _RX_TEMA.finditer(frase):
        t = _limpa_tema(m.group(1))
        # "o texto CB1A1 e a Lei n.º 8.112/1990" → as partes coordenadas são avaliadas separadamente
        partes = [p for p in re.split(r"\s+e\s+(?=(?:n?[oa]s?|à|às|ao|aos)\s)", t) if p]
        for p in partes:
            p = _limpa_tema(p)
            if len(p) < 3 or _DEITICO.match(p) or _SO_REFERENCIA.match(p):
                continue
            if p not in out:
                out.append(p)
    m = _RX_LING.search(frase)
    if m and not any(_RX_LING.search(t) for t in out):
        out.append(m.group(0))
    return out


def assunto_de(tipo: str, enunciado: str | None, comando: str | None) -> tuple[str | None, str | None]:
    """(assunto, frase_comando). CE/DISC: comando do bloco; ME: o próprio enunciado (ou o comando do bloco)."""
    frase = None
    if tipo == "ME":
        frase = _frase_comando(enunciado, r"assinale|indique|escolha")
        if not temas(frase):
            # "De acordo com o Código de Processo Civil, o pedido de gratuidade ... pode ser formulado"
            primeira = re.split(r"(?<=[.?!])\s+", limpa(enunciado or ""))[0] if enunciado else ""
            m = re.match(rf"^\s*((?:{_CONECT})\s+[^,]{{3,200}}),", primeira, re.I)
            if m:
                frase = m.group(1)
        if not temas(frase):
            frase = _frase_comando(comando) or frase
    else:
        frase = _frase_comando(comando)
    ts = temas(frase)
    return ("; ".join(ts) if ts else None), frase


# ------------------------------------------------------------------------------------------ disciplina
# (disciplina, regex sobre o texto normalizado: maiúsculas, sem acento). A ordem importa: a primeira regra que casa
# vence, então as mais específicas vêm antes (processo penal antes de penal, etc.).
REGRAS: list[tuple[str, str]] = [
    ("Língua Inglesa", r"\bLINGUA INGLESA\b|\bENGLISH\b|\bJUDGE THE\b|\bTEXT ABOVE\b"),
    ("Língua Espanhola", r"\bLINGUA ESPANHOLA\b|\bJUZGUE\b"),
    ("Língua Francesa", r"\bLINGUA FRANCESA\b"),
    ("Língua Portuguesa", r"\bLINGUA PORTUGUESA\b|\bLINGUISTIC|\bGRAMATIC|\bREDACAO OFICIAL\b|\bCORRESPONDENCIA OFICIAL\b|"
                          r"\bMANUAL DE REDACAO\b|\bCOMPREENSAO (?:E INTERPRETACAO )?DE TEXTO|\bINTERPRETACAO DE TEXTO|"
                          r"\bTIPOLOGIA TEXTUAL|\bGENEROS? TEXTUA|\bCOESAO (?:TEXTUAL|E (?:A )?COERENCIA|REFERENCIAL|SEQUENCIAL)|\bCOERENCIA TEXTUAL|\bANALISE SINTATICA|\bFUNCOES? SINTATICA|\bMORFOSSINT|\bCLASSES? (?:DE PALAVRAS|GRAMATICA)|"
                          r"\bASPECTOS SEMANTICOS|\bRELACOES SEMANTICAS|\bSINAIS DE PONTUACAO|\bEMPREGO DOS? SINA|\bCONCORDANCIA (?:VERBAL|NOMINAL)|\bREGENCIA (?:VERBAL|NOMINAL)|\bCRASE\b|"
                          r"\bORTOGRAFI|\bACENTUACAO GRAFICA|\bIDEIAS\b.*\bTEXTO\b|\bVOCABULARIO\b.*\bTEXTO\b|\bASPECTOS (?:DISCURSIVOS|GRAMATICAIS|"
                          r"SEMANTICOS|SINTATICOS|TEXTUAIS)|\bESTRUTURAS? LINGUISTIC|\bPROPRIEDADES LINGUISTIC|"
                          r"\bSENTIDOS? (?:DO|E D[AO]S?) TEXTO|\bPADRAO (?:CULTO|FORMAL)"),
    ("Raciocínio Lógico e Matemática", r"\bRACIOCINIO LOGIC|\bLOGICA (?:PROPOSICIONAL|SENTENCIAL|DE PRIMEIRA ORDEM|"
                                       r"MATEMATICA|DE ARGUMENTACAO)|\bPROPOSICOES LOGICAS|\bTABELAS?[ -]VERDADE|"
                                       r"\bANALISE COMBINATORIA|\bPROBABILIDADES?\b|\bPROGRESS(?:AO|OES) (?:ARITMETICA|GEOMETRICA)|"
                                       r"\bMATEMATICA (?:BASICA|FINANCEIRA)|\bJUROS (?:SIMPLES|COMPOSTOS)|\bTEORIA DOS CONJUNTOS|"
                                       r"\bRACIOCINIO (?:ANALITICO|MATEMATICO|SEQUENCIAL|QUANTITATIVO)|\bPORCENTAGE|\bREGRA DE TRES"),
    ("Estatística", r"\bESTATISTIC(?!O DE TRANSTORNOS)|\bREGRESSAO LINEAR|\bINTERVALO DE CONFIANCA|\bTESTES? DE HIPOTES|\bDISTRIBUICAO (?:NORMAL|"
                    r"BINOMIAL|DE POISSON|AMOSTRAL)|\bAMOSTRAGEM|\bVARIAVE(?:L|IS) ALEATORIA|\bINFERENCIA ESTAT|\bSERIES TEMPORA"),
    ("Educação e Pedagogia", r"\bBNCC\b|\bBASE NACIONAL COMUM CURRICULAR|\bDIDATICA|\bEDUCACAO (?:ESPECIAL|INCLUSIVA|INFANTIL)|"
                             r"\bLDB\b|\bDIRETRIZES E BASES DA EDUCACAO|\bPROJETO POLITICO.PEDAGOGICO|\bPEDAGOGI|"
                             r"\bPROCESSO (?:DE )?ENSINO.APRENDIZAGEM|\bAVALIACAO DA APRENDIZAGEM|\bCURRICULO\b"),
    ("Serviço Social", r"\bSERVICO SOCIAL|\bASSISTENTES? SOCIA|\bASSISTENCIA SOCIAL|\bLOAS\b|\bSISTEMA UNICO DE ASSISTENCIA SOCIAL"),
    ("Enfermagem", r"\bENFERMAG|\bENFERMEIR"),
    ("Psicologia", r"\bPSICOLOG|\bPSICOPATOLOG|\bPSICOTERAP|\bPSICODIAGNOST|\bAVALIACAO PSICOLOGICA"),
    ("Arquivologia", r"\bARQUIV|\bGESTAO DE DOCUMENTOS|\bTABELA DE TEMPORALIDADE|\bCLASSIFICACAO DE DOCUMENTOS|"
                     r"\bSERVICOS? DE PROTOCOLO|\bPROTOCOLO E ARQUIVO|\bDOCUMENTOS DE ARQUIVO"),
    ("Biblioteconomia", r"\bBIBLIOTECONOM|\bBIBLIOTECAS?\b(?! (?:CIENTIFICAS|NUMPY|PANDAS|PYTHON|JAVA|DE (?:SOFTWARE|CLASSES|FUNCOES|PROGRAMACAO)))|\bCATALOGA|\bINDEXACAO|\bAACR|\bMARC 21|\bCDD\b|\bCDU\b|\bREFERENCIA BIBLIOGRAF|"
                        r"\bNORMAS? DA ABNT PARA DOCUMENTACAO|\bCATALOGOS?\b"),
    ("Ética no Serviço Público", r"\bETICA (?:NO SERVICO PUBLICO|PUBLICA|NA ADMINISTRACAO PUBLICA)|\bCODIGO DE ETICA (?:PROFISSIONAL )?DO SERVIDOR|"
                                 r"\bDECRETO N 1 ?171|\bCONDUTA (?:ETICA )?DOS (?:SERVIDORES|AGENTES PUBLICOS)|\bCODIGO DE CONDUTA DA ALTA"),
    ("Direito Ambiental", r"\bDIREITO AMBIENTAL|\bLICENCIAMENTO AMBIENTAL|\bCRIMES AMBIENTAIS|\bPOLITICA NACIONAL DO MEIO AMBIENTE|"
                          r"\bCODIGO FLORESTAL|\bSNUC\b|\bUNIDADES DE CONSERVACAO|\bRESPONSABILIDADE (?:CIVIL )?AMBIENTAL"),
    ("Direito Processual Penal", r"\bPROCESS(?:O|UAL) PENAL\b|\bCODIGO DE PROCESSO PENAL\b|\bCPP\b|\bINQUERITO POLICIAL|"
                                 r"\bACAO PENAL|\bPRISAO (?:PREVENTIVA|TEMPORARIA|EM FLAGRANTE)|\bJURI\b|\bEXECUCAO PENAL|"
                                 r"\bLEI DE EXECUCAO PENAL|\bINTERCEPTACAO TELEFONICA"),
    ("Direito Processual do Trabalho", r"\bPROCESS(?:O|UAL) (?:DO )?TRABALH"),
    ("Direito Processual Civil", r"\bPROCESS(?:O|UAL) CIVIL\b|\bCODIGO DE PROCESSO CIVIL\b|(?<!CONTABEIS )\bCPC\b(?! \d)|\bTUTELAS? PROVISORIA|"
                                 r"\bRECURSOS? (?:CIVEIS|NO PROCESSO CIVIL)|\bCUMPRIMENTO DE SENTENCA|\bPETICAO INICIAL|"
                                 r"\bLITISCONSORCIO|\bCOISA JULGADA|\bSENTENCA E (?:D)?A COISA JULGADA|\bMANDADO DE SEGURANCA|"
                                 r"\bACAO CIVIL PUBLICA|\bJUIZADOS? ESPECIA(?:L|IS) CIVE|\bGRATUIDADE DA JUSTICA"),
    ("Direito Penal", r"\bDIREITO PENAL\b|\bCODIGO PENAL\b|\bCRIMES?\b|\bPENAL\b|\bLEI DE DROGAS|\bLEI MARIA DA PENHA|"
                      r"\bIMPUTABILIDADE|\bTIPICIDADE|\bDOSIMETRIA|\bLEGISLACAO PENAL|\bLEI (?:N \d+ )?DOS CRIMES"),
    ("Direito Tributário", r"\bTRIBUT|\bIMPOSTOS?\b|\bICMS\b|\bIPVA\b|\bITCMD|\bISS\b|\bIPTU\b|\bIRPF\b|\bIRPJ\b|\bIRRF\b|"
                           r"\bCODIGO TRIBUTARIO|\bCTN\b|\bCREDITO TRIBUTARIO|\bLANCAMENTO TRIBUTARIO|\bTAXAS? E CONTRIBUICO|"
                           r"\bCONTRIBUICOES? SOCIA|\bRETENC(?:AO|OES) NA FONTE|\bIBS\b|\bCBS\b|\bOBRIGACAO TRIBUTARIA|\bSIMPLES NACIONAL|\bIMPOSTO DE RENDA"),
    ("Direito Previdenciário", r"\bPREVIDENCI|\bSEGURIDADE SOCIAL|\bREGIME GERAL DE PREVIDENCIA|\bRGPS\b|\bRPPS\b|"
                               r"\bBENEFICIOS? PREVIDENCI|\bAPOSENTADORIA"),
    ("Direito do Trabalho", r"\bDIREITO (?:INDIVIDUAL |COLETIVO )?DO TRABALHO\b|\bCLT\b|\bCONSOLIDACAO DAS LEIS DO TRABALHO|"
                            r"\bCONTRATO (?:INDIVIDUAL )?DE TRABALHO|\bJORNADA DE TRABALHO|\bRELACAO DE EMPREGO|\bTERCEIRIZACAO|"
                            r"\bREFORMA TRABALHISTA|\bTRABALHIST"),
    ("Direito Eleitoral", r"\bELEITORA|\bELEICO|\bPARTIDOS? POLITICOS|\bCODIGO ELEITORAL|\bJUSTICA ELEITORAL"),
    ("Direito Empresarial", r"\bEMPRESARIA|\bSOCIEDADES? (?:ANONIMAS?|LIMITADAS?|EMPRESARIAS?)|\bTITULOS? DE CREDITO|"
                            r"\bFALENCIA|\bPROPRIEDADE INTELECTUAL|\bPATENTES?\b|\bRECUPERACAO JUDICIAL|\bDIREITO COMERCIAL|\bPROPRIEDADE INDUSTRIAL"),
    ("Direito do Consumidor", r"\bDIREITO DO CONSUMIDOR|\bDEFESA DO CONSUMIDOR|\bRELACOES? DE CONSUMO|\bCDC\b"),
    ("Direito Financeiro e Orçamento Público", r"\bDIREITO FINANCEIRO|\bORCAMENTO PUBLICO|\bORCAMENTARI|\bFUNCOES DO ORCAMENTO|\bORCAMENTO (?:DA UNIAO|GERAL|FISCAL|DE INVESTIMENTO|DA SEGURIDADE)|\bLEI DE RESPONSABILIDADE FISCAL|\bLRF\b|"
                                               r"\bLEI COMPLEMENTAR N 101|\bLEI N 4 ?320|\bRECEITAS? PUBLICAS?|\bDESPESAS? PUBLICAS?|"
                                               r"\bPPA\b|\bLDO\b|\bLOA\b|\bCREDITOS ADICIONAIS|\bEMPENHO|\bRESTOS A PAGAR|"
                                               r"\bPRECATORIO|\bDIVIDA PUBLICA|\bFINANCAS PUBLICAS|\bAFO\b"),
    ("Auditoria", r"\bAUDITORIA|\bAUDITOR\b|\bNBC ?TA\b|\bNORMAS DE AUDITORIA|\bPAPEIS DE TRABALHO"),
    ("Contabilidade Pública", r"\bCONTABILIDADE (?:PUBLICA|APLICADA AO SETOR PUBLICO)|\bMCASP\b|\bNBC ?T ?SP|\bPCASP\b|"
                              r"\bSIAFI\b|\bDEMONSTRACOES CONTABEIS APLICADAS AO SETOR PUBLICO"),
    ("Contabilidade", r"\bCONTABI|\bCONTABE|\bBALANCO PATRIMONIAL|\bDEMONSTRACAO D[OE]S? (?:RESULTADO|FLUXOS? DE CAIXA)|\bDRE\b|"
                      r"\bCPC \d+|\bPRONUNCIAMENTOS? (?:TECNICOS? )?(?:DO )?CPC|\bATIVO (?:IMOBILIZADO|INTANGIVEL)|"
                      r"\bDEPRECIAC|\bCUSTOS? (?:INDUSTRIAIS|DE PRODUCAO)|\bCONTABILIDADE DE CUSTOS|"
                      r"\bANALISE DAS DEMONSTRACOES|\bPATRIMONIO LIQUIDO|\bLANCAMENTOS? CONTABE"),
    ("Controle Externo", r"\bCONTROLE EXTERNO|\bTRIBUNA(?:L|IS) DE CONTAS|\bTCU\b|\bTCE\b|\bTCM\b|\bLEI ORGANICA DO TC|"
                         r"\bREGIMENTO INTERNO DO TC|\bFISCALIZACOES? REALIZADAS PELO TC|\bPRESTACAO DE CONTAS|"
                         r"\bTOMADA DE CONTAS"),
    ("Direito Constitucional", r"\bCONSTITUC|\bCONSTITUICAO|\bCF\b|\bCF ?1988|\bDIREITOS (?:E GARANTIAS )?FUNDAMENTAIS|"
                               r"\bREMEDIOS CONSTITUCIONAIS|\bHABEAS (?:CORPUS|DATA)|\bMANDADO DE INJUNCAO|"
                               r"\bORGANIZACAO (?:DO ESTADO|DOS PODERES|POLITICO.ADMINISTRATIVA)|\b(?:ATRIBUICOES|COMPETENCIAS|ORGANIZACAO) DO PODER (?:LEGISLATIVO|"
                               r"EXECUTIVO|JUDICIARIO)|\bPROCESSO LEGISLATIVO|\bCONTROLE DE CONSTITUCIONALIDADE|"
                               r"\bFUNCOES ESSENCIAIS A JUSTICA|\bPODER CONSTITUINTE|\bNACIONALIDADE|\bDIREITOS POLITICOS|\bLEI ORGANICA DO DISTRITO"),
    ("Direito Administrativo", r"\bADMINISTRATIV|\bATOS? ADMINISTRATIV|\bLICITAC|\bLEI N 14 ?133|\bLEI N 8 ?666|\bCONTRATOS? "
                               r"ADMINISTRATIV|\bCONTRATACOES? PUBLICAS|\bSERVIDOR(?:ES)? PUBLIC|\bLEI N 8 ?112|\bREGIME "
                               r"JURIDICO|\bAGENTES PUBLICOS|\bPODERES? (?:DA ADMINISTRACAO|ADMINISTRATIV|DE POLICIA|"
                               r"HIERARQUICO|DISCIPLINAR)|\bIMPROBIDADE|\bLEI N 8 ?429|\bRESPONSABILIDADE CIVIL DO ESTADO|"
                               r"\bSERVICOS PUBLICOS|\bCONCESS(?:AO|OES)|\bPARCERIAS? PUBLICO.PRIVADA|\bBENS PUBLICOS|"
                               r"\bINTERVENCAO DO ESTADO NA PROPRIEDADE|\bDESAPROPRIA|\bPROCESSO ADMINISTRATIVO|\bLEI N 9 ?784|"
                               r"\bADMINISTRACAO (?:DIRETA|INDIRETA)|\bAUTARQUIA|\bEMPRESAS? (?:PUBLICAS|ESTATAIS)|"
                               r"\bLEI N 13 ?303|\bACESSO A INFORMACAO|\bLEI N 12 ?527|\bPROCESSO ADMINISTRATIVO DISCIPLINAR|"
                               r"\bREGIME DISCIPLINAR|\bLEI ANTICORRUPCAO|\bLEI N 12 ?846|\bCONTROLE DA ADMINISTRACAO"),
    ("Direito Civil", r"\bDIREITO CIVIL\b|\bCODIGO CIVIL\b|\bNEGOCIOS? JURIDICOS?|\bOBRIGACOES\b|\bCONTRATOS? (?:CIVIS|EM "
                      r"ESPECIE)|\bRESPONSABILIDADE CIVIL\b|\bDIREITOS? REAIS|\bPOSSE\b|\bPROPRIEDADE\b|\bUSUCAPIAO|"
                      r"\bDIREITO DE FAMILIA|\bDIREITO DAS SUCESSOES|\bSUCESSOES?\b|\bPRESCRICAO E DECADENCIA|"
                      r"\bPESSOAS? (?:NATURA(?:L|IS)|JURIDICAS?)|\bLINDB\b|\bLEI DE INTRODUCAO"),
    ("Direitos Humanos", r"\bDIREITOS HUMANOS|\bPACTO DE SAO JOSE|\bCONVENCAO AMERICANA|\bDECLARACAO UNIVERSAL"),
    ("Direito Internacional", r"\bDIREITO INTERNACIONAL|\bTRATADOS INTERNACIONAIS"),
    ("Direito da Criança e do Adolescente", r"\bESTATUTO DA CRIANCA|\bECA\b|\bCRIANCA E DO ADOLESCENTE|\bATO INFRACIONAL"),
    ("Gestão de Pessoas", r"\bGESTAO DE PESSOAS|\bRECURSOS HUMANOS|\bRECRUTAMENTO|\bSELECAO DE PESSOAL|\bAVALIACAO DE DESEMPENHO|"
                          r"\bTREINAMENTO E DESENVOLVIMENTO|\bCOMPORTAMENTO ORGANIZACIONAL|\bCLIMA ORGANIZACIONAL|"
                          r"\bCULTURA ORGANIZACIONAL|\bMOTIVACAO\b|\bLIDERANCA\b|\bGESTAO POR COMPETENCIAS"),
    ("Administração Pública", r"\bADMINISTRACAO PUBLICA\b|\bGESTAO PUBLICA|\bPOLITICAS PUBLICAS|\bGOVERNANCA PUBLICA|"
                              r"\bNOVA GESTAO PUBLICA|\bGOVERNANCA (?:NO SETOR PUBLICO|PUBLICA)|\bREFORMAS? (?:ADMINISTRATIVAS?|DO ESTADO)|\bMODELOS? DE ADMINISTRACAO "
                              r"PUBLICA|\bGOVERNO ELETRONICO|\bACCOUNTABILITY|\bPLANEJAMENTO GOVERNAMENTAL"),
    ("Administração Geral", r"\bADMINISTRACAO GERAL|\bTEORIAS? (?:GERAL )?DA ADMINISTRACAO|\bFUNCOES DA ADMINISTRACAO|\bESCOLAS? DA ADMINISTRACAO|"
                            r"\bGERENCIAMENTO DE PROJETOS|\bGESTAO DO CONHECIMENTO|\bCICLO PDCA|\bPLANEJAMENTO ESTRATEGICO|\bGESTAO DE PROCESSOS|\bGESTAO DE "
                            r"PROJETOS|\bPMBOK|\bGESTAO DA QUALIDADE|\bBALANCED SCORECARD|\bGESTAO DE RISCOS|"
                            r"\bESTRUTURA ORGANIZACIONAL|\bPROCESSO ORGANIZACIONAL|\bGESTAO ESTRATEGICA|\bGOVERNANCA CORPORATIVA|"
                            r"\bDESIGN THINKING|\bOKR\b|\bGESTAO DE CONTRATOS|\bLOGISTICA|\bGESTAO DE MATERIAIS|"
                            r"\bADMINISTRACAO DE (?:MATERIAIS|RECURSOS MATERIAIS)|\bCOMPRAS\b"),
    ("Economia", r"\bECONOMIA\b|\bMACROECON|\bMICROECON|\bINFLACAO|\bPOLITICA (?:MONETARIA|FISCAL|CAMBIAL)|\bPIB\b|"
                 r"\bMERCADO FINANCEIRO|\bSISTEMA FINANCEIRO NACIONAL|\bBANCO CENTRAL|\bTAXAS? DE (?:JUROS|CAMBIO)|"
                 r"\bELASTICIDADE|\bOFERTA E (?:A )?DEMANDA|\bCOMERCIO INTERNACIONAL|\bFINANCAS CORPORATIVAS"),
    ("Tecnologia da Informação", r"\bBANCOS? DE DADOS|\bSQL\b|\bMODELAGEM DE DADOS|\bENTIDADE.RELACIONAMENTO|\bREDES DE "
                                 r"COMPUTADORES|\bPROTOCOLOS?\b.*\b(?:TCP|IP|HTTP|DNS|ROTEAMENTO)|\bTCP\b|\bDNS\b|\bROTEAMENTO|"
                                 r"\bSEGURANCA DA INFORMACAO|\bCRIPTOGRAF|\bFIREWALL|\bMALWARE|\bLINGUAGEM (?:R|PYTHON|JAVA|C)\b|"
                                 r"\bPYTHON\b|\bNUMPY\b|\bPANDAS\b|\bJAVA\b|\bJAVASCRIPT|\bLOGICA DE PROGRAMACAO|"
                                 r"\bLINGUAGE(?:M|NS) DE PROGRAMACAO|\bPROGRAMACAO (?:ORIENTADA|ESTRUTURADA|FUNCIONAL|WEB)|"
                                 r"\bALGORITMOS?\b|\bESTRUTURAS? DE DADOS|"
                                 r"\bENGENHARIA DE SOFTWARE|\bDESENVOLVIMENTO (?:DE SOFTWARE|AGIL)|\bSCRUM|\bKANBAN|\bDEVOPS|"
                                 r"\bITIL\b|\bCOBIT\b|\bGOVERNANCA DE TI|\bCOMPUTACAO EM NUVEM|\bCLOUD\b|\bBUSINESS INTELLIGENCE|"
                                 r"\bBI\b|\bDATA WAREHOUSE|\bBIG DATA|\bCIENCIA DE DADOS|\bAPRENDIZADO DE MAQUINA|\bMACHINE "
                                 r"LEARNING|\bINTELIGENCIA ARTIFICIAL|\bMINERACAO DE DADOS|\bSISTEMAS? OPERACIONA|\bLINUX\b|"
                                 r"\bVIRTUALIZACAO|\bDOCKER|\bKUBERNETES|\bARQUITETURA DE (?:SOFTWARE|"
                                 r"COMPUTADORES)|\bTESTES? DE SOFTWARE|\bUML\b|\bAPIS?\b|\bWEB SERVICES?|\bMFA\b|"
                                 r"\bANALISE FORENSE|\bCIBERNETIC|\bINCIDENTES? DE SEGURANCA|\bQUALIDADE DE SOFTWARE|\bENGENHARIA DE REQUISITOS|\bMETODOLOGIAS AGEIS|"
                                 r"\bAMEACAS E VULNERABILIDADES|\bVULNERABILIDADES? (?:DE|EM) (?:SEGURANCA|SOFTWARE|APLICAC|SISTEMAS|REDES)|\bLGPD\b|\bPROTECAO DE DADOS PESSOAIS|\bTECNOLOGIA DA INFORMACAO"),
    ("Noções de Informática", r"\bNOCOES DE INFORMATICA|\bINFORMATICA\b|\bMICROSOFT (?:OFFICE|WORD|EXCEL|365|TEAMS)|"
                              r"\b(?:MS )?(?:WORD|EXCEL|POWERPOINT|LIBREOFFICE|WRITER|CALC)\b|\bNAVEGADORES?\b|\bCORREIO "
                              r"ELETRONICO|\bWINDOWS\b|\bINTERNET E INTRANET|\bEDITORES? DE TEXTO|\bPLANILHAS? ELETRONICA"),
    ("Saúde Pública e SUS", r"\bSUS\b|\bSISTEMA UNICO DE SAUDE|\bSAUDE (?:PUBLICA|COLETIVA)|\bVIGILANCIA (?:EM SAUDE|"
                            r"EPIDEMIOLOGICA|SANITARIA)|\bEPIDEMIOLOG|\bATENCAO (?:BASICA|PRIMARIA)|\bPOLITICAS? (?:PUBLICAS? )?DE "
                            r"SAUDE|\bLEI N 8 ?080|\bLEI N 8 ?142|\bMORBIDADE|\bMORTALIDADE"),
    ("Legislação de Trânsito", r"\bCODIGO DE TRANSITO|\bCTB\b|\bLEGISLACAO DE TRANSITO|\bINFRACOES DE TRANSITO"),
    ("Legislação Específica", r"\bLEGISLACAO (?:ESPECIFICA|INSTITUCIONAL|APLICADA|ESTADUAL|DISTRITAL|MUNICIPAL)|"
                              r"\bREGIMENTO INTERNO|\bLEI ORGANICA\b|\bESTATUTO DOS SERVIDORES"),
    ("Atualidades e Realidade Regional", r"\bATUALIDADES|\bREALIDADE (?:ETNICA|HISTORICA|GEOGRAFICA|CULTURAL|"
                                         r"POLITICA|ECONOMICA)|\bHISTORIA E GEOGRAFIA D[OE]|\bCONHECIMENTOS SOBRE O (?:ESTADO|"
                                         r"MUNICIPIO|DISTRITO FEDERAL)"),
    ("Sustentabilidade", r"\bSUSTENTABILIDADE|\bDESENVOLVIMENTO SUSTENTAVEL|\bAGENDA 2030|\bODS\b"),
]
_REGRAS = [(d, re.compile(rx)) for d, rx in REGRAS]

# títulos de bloco que já são o nome de uma disciplina (fonte titulo_pdf); usa a mesma tabela
_TITULO_DISCIPLINA = re.compile(r"^(?:PROVA (?:ESCRITA |OBJETIVA )?DE |CONHECIMENTOS DE |NOCOES DE )?"
                                r"(?:L[IÍ]NGUA|RACIOC|NOCOES|DIREITO|LEGISLA|INFORMAT|MATEMAT|ESTATIST|CONTABI|ECONOMI|"
                                r"ADMINISTRA|ARQUIV|ETICA|ATUALIDADES|AUDITORIA|REALIDADE)")


def norm_regra(t: str | None) -> str:
    """Texto como as regras o veem: norm() + "Lei n.º 8.112/1990" → "LEI N 8 112 1990" (sem pontuação)."""
    s = norm(t)
    s = re.sub(r"\bN\s*\.?\s*[O°º]?\s*\.?\s*(?=\d)", "N ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def disciplina_por_texto(t: str | None) -> str | None:
    s = norm_regra(t)
    if not s:
        return None
    for d, rx in _REGRAS:
        if rx.search(s):
            return d
    return None


def disciplina_de(variante: str | None, secao: str | None, assunto: str | None,
                  frase: str | None = None) -> tuple[str | None, str | None]:
    """(disciplina, fonte): variante > titulo_pdf > regra_comando (idioma do comando) > regra_assunto."""
    if variante:
        d = disciplina_por_texto(variante)
        if d:
            return d, "variante"
    s = norm(secao)
    if s and _TITULO_DISCIPLINA.match(s):
        d = disciplina_por_texto(s)
        if d:
            return d, "titulo_pdf"
    if frase and _RX_INGLES.search(frase):
        return "Língua Inglesa", "regra_comando"
    if frase and _RX_ESPANHOL.search(frase):
        return "Língua Espanhola", "regra_comando"
    if assunto:
        d = disciplina_por_texto(assunto)
        if d:
            return d, "regra_assunto"
    return None, None


_MINUSC = {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "na", "no", "nas", "nos", "à", "ao", "aos",
           "às", "com", "para", "por"}


def nome_legivel(s: str) -> str:
    """"TRANSPORTES  AQUAVIÁRIOS" → "Transportes Aquaviários" (nomes do edital fora da tabela de regras)."""
    s = re.sub(r"\s+", " ", s).strip()
    if s != s.upper():
        return s
    ps = s.lower().split(" ")
    return " ".join(p if (k and p in _MINUSC) else (p[:1].upper() + p[1:]) for k, p in enumerate(ps))


def combinar(d_regra: str | None, f_regra: str | None, nome_edital: str | None,
             f_edital: str | None) -> tuple[str | None, str | None]:
    """Precedência final: variante > titulo_pdf > regra_comando > edital_assunto > regra_assunto > edital_unica >
    area_prova. A disciplina vinda do edital é padronizada pela tabela de regras quando possível."""
    if f_regra in ("variante", "titulo_pdf", "regra_comando"):
        return d_regra, f_regra
    pad = (disciplina_por_texto(nome_edital) or nome_legivel(nome_edital)) if nome_edital else None
    if f_edital == "edital_assunto":
        return pad, f_edital
    if f_regra == "regra_assunto":
        return d_regra, f_regra
    if f_edital in ("edital_unica", "area_prova"):
        return pad, f_edital
    return None, None


# ----------------------------------------------------------------------------------------------- execução
def classificar(con, slugs=None, ano=None, desde=None, usar_edital: bool = True) -> dict:
    """Recalcula bloco, assunto e disciplina das questões selecionadas (idempotente)."""
    from . import edital as ed
    q = """SELECT q.id, q.tipo, q.variante, q.secao, q.enunciado, t.tipo AS tb_tipo, t.conteudo AS tb,
                  p.concurso_id, p.cargo, d.descricao AS doc_desc,
                  (SELECT group_concat(pc.cargo, '|') FROM prova_cargo pc WHERE pc.prova_id=p.id) AS cargos_prova
           FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
           JOIN documento d ON d.id=p.documento_id
           LEFT JOIN texto_base t ON t.id=q.texto_base_id WHERE 1=1"""
    args: list = []
    if slugs:
        q += f" AND c.slug IN ({','.join('?' * len(slugs))})"
        args += slugs
    if ano:
        q += " AND c.ano=?"
        args.append(ano)
    if desde:
        q += " AND c.ano>=?"
        args.append(desde)
    st = {"questoes": 0, "com_bloco": 0, "com_assunto": 0, "com_disciplina": 0, "por_fonte": {},
          "concursos_com_edital": 0, "concursos_sem_edital": 0}
    sql_up = ("UPDATE questao SET bloco=?, assunto=?, disciplina=?, disciplina_fonte=?, disciplina_edital=? "
              "WHERE id=?")
    lote: list[tuple] = []
    classif: dict[int, object] = {}          # concurso_id → Classificador | None (sem edital lido)
    for r in con.execute(q + " ORDER BY p.concurso_id", args).fetchall():
        b = bloco(r["secao"], r["tipo"])
        comando = r["tb"] if r["tb"] and len(r["tb"]) < 4000 else (r["tb"][-1500:] if r["tb"] else None)
        assunto, frase = assunto_de(r["tipo"], r["enunciado"], comando)
        d_regra, f_regra = disciplina_de(r["variante"], r["secao"], assunto, frase)
        nome_ed, f_ed = None, None
        if usar_edital:
            cid = r["concurso_id"]
            if cid not in classif:
                ents = ed.ler_edital(con, cid)
                classif[cid] = ed.Classificador(ents) if ents else None
                st["concursos_com_edital" if classif[cid] is not None and classif[cid].e else "concursos_sem_edital"] += 1
            cl = classif[cid]
            cargos, area = ed.cargo_area(r["cargo"])
            for pc in (r["cargos_prova"] or "").split("|"):
                cargos |= ed.cargo_area(pc)[0]
            if not cargos or area is None:          # "PROVA OBJETIVA - CONHECIMENTOS ESPECÍFICOS - ÁREA 6"
                c2, a2 = ed.cargo_area(r["doc_desc"])
                cargos = cargos or c2
                area = area if area is not None else a2
            motivo = "sem_edital"
            if cl is not None and cl.e:
                nome_ed, motivo, _ = cl.classificar(assunto, cargos, area, b)
            if nome_ed:
                f_ed = motivo
            elif motivo == "sem_edital" and b not in ("basicos", "gerais"):
                # concurso sem conteúdo programático (ex.: residências): área declarada pela própria prova
                # ("ÁREA PROFISSIONAL: NUTRIÇÃO"), só fora dos blocos básicos/gerais e se o rótulo for uma área de
                # conhecimento (não "ÁREA: ADMINISTRATIVA", "ÁREA: JUDICIÁRIA" ...)
                nome_ed = ed.rotulo_area(r["doc_desc"]) or ed.rotulo_area(r["cargo"])
                if nome_ed and ed.rotulo_generico(nome_ed):
                    nome_ed = None
                f_ed = "area_prova" if nome_ed else None
        d, fonte = combinar(d_regra, f_regra, nome_ed, f_ed)
        lote.append((b, assunto, d, fonte, nome_ed if d is not None and f_ed else None, r["id"]))
        st["questoes"] += 1
        st["com_bloco"] += b is not None
        st["com_assunto"] += assunto is not None
        st["com_disciplina"] += d is not None
        if fonte:
            st["por_fonte"][fonte] = st["por_fonte"].get(fonte, 0) + 1
        if len(lote) >= 5000:
            con.executemany(sql_up, lote)
            lote.clear()
    if lote:
        con.executemany(sql_up, lote)
    con.commit()
    return st
