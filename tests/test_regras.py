from cebraspe_bank import anos
from cebraspe_bank.classify import classificar, codigo_prova
from cebraspe_bank.texto import norm


def test_slug():
    assert anos.slug_tokens("CAPES_23") == ("CAPES", 2023)
    assert anos.slug_tokens("INSS_2015") == ("INSS", 2015)
    assert anos.slug_tokens("PREF_SALVADOR_15_PROCURADOR") == ("PREF_SALVADOR", 2015)
    assert anos.slug_tokens("SES_DF_15_MULTIPROFISSIONAL_2") == ("SES_DF", 2015)
    assert anos.slug_tokens("PC_GO_DELEGADO_16") == ("PC_GO_DELEGADO", 2016)


def test_edital_nome_e_texto():
    assert anos.ano_nome_edital("ED_1_2023_CAPES_ABERTURA.PDF") == 2023
    assert anos.ano_nome_edital("ED_1_AEB_24_ABERTURA.PDF") is None
    t = norm("EDITAL Nº 1 – CAPES, DE 14 DE DEZEMBRO DE 2023\nAplicação: 17/3/2024")
    assert anos.data_edital_texto(t) == "2023-12-14"
    assert anos.data_aplicacao_texto("Aplicação: 17/3/2024") == "2024-03-17"
    assert anos.ano_aplicacao_texto("CESPE | CEBRASPE – INSS – Aplicação: 2016") == 2016


def test_precedencia():
    assert anos.resolver({"slug": 2024, "edital_publicacao": 2023}) == (2023, "edital_publicacao")
    assert anos.resolver({"slug": 2024, "aplicacao": 2025}) == (2024, "slug")
    assert anos.resolver({"aplicacao": 2025}) == (2025, "aplicacao")
    assert anos.resolver({}) == (None, None)


def test_codigo_prova():
    assert codigo_prova("947_CAPES_001_01.PDF") == ("947_CAPES_001_01", "001")
    assert codigo_prova("GAB_DEFINITIVO_947_CAPES_001_01.PDF") == ("947_CAPES_001_01", "001")
    assert codigo_prova("234INSS_001_01_Caderno_LUA.PDF") == ("234INSS_001_01", "001")
    assert codigo_prova("Gab_Definitivo_234INSS_001_01.PDF") == ("234INSS_001_01", "001")
    assert codigo_prova("MATRIZ_039_CAESB_CG1_00_Com Justificativas_atualizado.pdf") == ("039_CAESB_CG1_00", "CG1")
    assert codigo_prova("Gab_Definitivo_MATRIZ_039_CAESB_CG1_00.pdf") == ("039_CAESB_CG1_00", "CG1")
    assert codigo_prova("378_ABIN_DISC_013_01.PDF")[1] == "DISC"
    assert codigo_prova("947_CAPES_001_DISC.PDF")[1] == "DISC"
    assert codigo_prova("5B0C591D4033C261FC602C2A3E48D29E9DC447ECB4A2845D17E7652B2B8A7100.pdf") == (None, None)


def test_classificacao():
    c = classificar("234INSS_001_01_Caderno_LUA.PDF", "Caderno de provas - Cargo 1: Caderno LUA")
    assert (c.tipo, c.caderno, c.cargo) == ("prova", "LUA", "Cargo 1")
    assert classificar("GAB_PRELIMINAR_657_TELEBRAS_CB1_01.PDF", "GABARITO PRELIMINAR - CONHECIMENTOS BÁSICOS").tipo == "gabarito_preliminar"
    assert classificar("x.pdf", "GABARITO DEFINITIVO - PROVA OBJETIVA - CONHECIMENTOS GERAIS").tipo == "gabarito_definitivo"
    assert classificar("x.pdf", "PROVA E GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS - CARGO 1").tipo == "prova_com_gabarito_definitivo"
    assert classificar("x.pdf", "PROVA OBJETIVA (P1) E GABARITO PRELIMINAR COM JUSTIFICATIVAS - CARGOS 1 AO 18").tipo == "prova_com_gabarito_preliminar"
    assert classificar("TRE_BA_17_JUSTIFICATIVAS.PDF", "Justificativas de alteração de gabarito").tipo == "justificativa"
    assert classificar("PADRAORESPOSTA_947001A04.PDF", "PADRÃO DEFINITIVO DE RESPOSTA - PROVA DISCURSIVA - CARGO 1").tipo == "padrao_resposta"
    assert classificar("378_ABIN_CB1_010_SUPER.PDF", "PROVA OBJETIVA - CARGO 1 - SUPERAMPLIADA").acessibilidade
    assert classificar("x.pdf", "Edital nº 1 – Abertura").tipo == "edital_abertura"
    assert classificar("x.pdf", "Respostas às impugnações do edital de abertura").tipo == "edital"
    assert classificar("x.pdf", "CADERNO DE PROVA - 16: PROFESSOR (SALAS DE RECURSOS)").tipo == "prova"
    assert classificar("Malote1.pdf", "questões - prova oral - malote 1").tipo == "outro"
    assert classificar("x.pdf", "Relação final dos candidatos com a inscrição deferida").tipo == "outro"
    # provas de resposta livre que não dizem "discursiva"; capa; justificativas que citam "prova objetiva"
    assert classificar("x.pdf", "PROVA PRÁTICA (P3)").modalidade == "discursiva"
    assert classificar("x.pdf", "PROVA PRÁTICA DE SENTENÇA (P3) - SENTENÇA CÍVEL").modalidade == "discursiva"
    assert classificar("688_MPCE_TRIBUNA_001.PDF", "CASO HIPOTÉTICO 1 (TEMA)").modalidade == "discursiva"
    assert classificar("x.pdf", "Edital nº 24 – Resultado provisório na prova de tribuna").tipo == "edital"
    assert classificar("292_PMBH_CAPA_NS.pdf", "Caderno de provas - Capa").tipo == "outro"
    assert classificar("x.pdf", "Justificativas de alteração do gabarito da prova objetiva").tipo == "justificativa"
    assert classificar("x.pdf", "PROVA OBJETIVA (P1) E GABARITO PRELIMINAR COM JUSTIFICATIVAS").tipo == \
        "prova_com_gabarito_preliminar"
    # edital que publica o próprio gabarito (DPE_RS_21: tabela só como imagem); editais de recurso continuam editais
    assert classificar("ED_8_DPRS_2021_GABARITOS.PDF", "Edital nº 8 – Gabaritos oficiais preliminares da prova objetiva"
                       ).tipo == "gabarito_preliminar"
    assert classificar("x.pdf", "Edital nº 9 - Reabertura do prazo para interposição de recursos contra os gabaritos "
                                "oficiais preliminares").tipo == "edital"


def test_lingua_variantes():
    from cebraspe_bank.extract.gabarito import _rotulo
    from cebraspe_bank.extract.prova import norm_lingua
    from cebraspe_bank.extract import _resposta
    assert norm_lingua("Língua Espanhola ") == "LÍNGUA ESPANHOLA"
    leg = {(1.0, 0.0, 0.0): "LÍNGUA INGLESA", (0.31, 0.51, 0.74): "LÍNGUA ESPANHOLA"}
    assert _rotulo((1.0, 0.0, 0.0), leg) == "LÍNGUA INGLESA"
    assert _rotulo((0.0, 0.44, 0.75), leg) == "LÍNGUA ESPANHOLA"     # tom diferente da amostra da legenda
    assert _rotulo((0.5, 0.5, 0.5), {(1.0, 0.0, 0.0): "A", (0.0, 0.0, 1.0): "B"}) is None
    mapa = {("", 11): "C", ("LÍNGUA INGLESA", 1): "E", ("LÍNGUA ESPANHOLA", 1): "C"}
    assert _resposta(mapa, "LÍNGUA INGLESA", 1) == "E"
    assert _resposta(mapa, "", 1) is None                 # item comum não herda resposta de uma língua
    assert _resposta({("", 1): "C"}, "LÍNGUA INGLESA", 1) == "C"   # gabarito sem variantes


def test_alteracoes_diario_oficial():
    from cebraspe_bank.extract.gabarito import alteracoes
    t = ("Questões:\nQuestão 12 \nAnulada \nVersão de prova 1.1\nQuestão 13 \nAlterada de D p/ B \n"
         "Versão de prova 1.1\nQuestão 13 \nAlterada de B p/ E \nVersão de prova 1.2\n")
    assert alteracoes(t) == {"1.1": {12: (None, "X"), 13: ("D", "B")}, "1.2": {13: ("B", "E")}}


def test_vinculo_versao_e_secao():
    from cebraspe_bank.extract import _mesma_aplicacao, _secao_compativel, _sufixo_codigo, _versao_caderno
    assert _versao_caderno("1.3") == 3 and _versao_caderno("4") == 4 and _versao_caderno("LUA") is None
    assert _sufixo_codigo("254PMSP_CG1_03") == 3 and _sufixo_codigo("579_ANM") is None
    assert _mesma_aplicacao("579_ANM", "579_ANM_001_00") and not _mesma_aplicacao("614_SEFAZ_RR", "015_SEFAZRR21CF_001_01")
    assert _mesma_aplicacao(None, "579_ANM_001_00")
    esp = "GABARITO DEFINITIVO - CONHECIMENTOS ESPECIALIZADOS (PROVA OBJETIVA P3) - CARGO 1"
    assert not _secao_compativel(esp, [norm("CONHECIMENTOS BÁSICOS")])
    assert _secao_compativel(esp, [norm("CONHECIMENTOS ESPECIALIZADOS"), ""])
    assert _secao_compativel("GABARITO DEFINITIVO - PROVA OBJETIVA", [norm("CONHECIMENTOS BÁSICOS")])


def test_segmentacao():
    from cebraspe_bank.extract.gabarito import _linha_numeros
    from cebraspe_bank.extract.pdf import _agrupa_linhas
    from cebraspe_bank.extract.prova import Item, _corrige_numero_isolado
    itens = [Item(n, "ME") for n in (33, 344, 35)]
    av = []
    _corrige_numero_isolado(itens, av)
    assert [it.numero for it in itens] == [33, 34, 35] and av
    # última linha do gabarito completada com zeros: "Questão 59 60 0 0 0 ..."
    lw = [(0, 0, 30, 10, "Questão"), (40, 0, 50, 10, "59"), (60, 0, 70, 10, "60")] + \
         [(80 + 20 * i, 0, 90 + 20 * i, 10, "0") for i in range(18)]
    assert [w[4] for w in _linha_numeros(lw)] == ["59", "60"]
    lw1 = [lw[0], (40, 0, 50, 10, "100")] + lw[3:]
    assert [w[4] for w in _linha_numeros(lw1)] == ["100"]
    # glifo de fórmula com caixa de várias linhas não funde as linhas vizinhas
    ws = [(0, 0, 10, 10, "a"), (0, 14, 10, 24, "b"), (0, 28, 10, 38, "c"), (20, -10, 30, 48, "𝑈")]
    assert len(_agrupa_linhas(ws)) == 3


def test_justificativas_identificadores():
    from cebraspe_bank.extract import _ids_secao, _mesmas_questoes
    assert _ids_secao("CARGO 8: MÉDICO – ESPECIALIDADE: DERMATOLOGISTA") == {("CARGO", "8")}
    assert _ids_secao("OPÇÃO 40002042: ANALISTA – ÁREA: CIÊNCIA") == {("OPCAO", "40002042")}
    assert _ids_secao("PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE ANALISTA, EXCETO PARA O CARGO 4") == set()
    assert _ids_secao("PROVA OBJETIVA - CARGO 10") != _ids_secao("PROVA OBJETIVA - CARGO 1")
    # listas no plural: a seção casa com a prova da mesma lista, não com a de um emprego só
    sec = _ids_secao("CONHECIMENTOS BÁSICOS PARA OS EMPREGOS 2 E 5 A 8")
    assert sec == {("EMPREGO", str(n)) for n in (2, 5, 6, 7, 8)}
    assert sec <= _ids_secao("PROVA OBJETIVA – CONHECIMENTOS BÁSICOS – EMPREGOS 2 E 5 A 8")
    assert not sec <= _ids_secao("PROVA OBJETIVA – CONHECIMENTOS ESPECÍFICOS – EMPREGO 2")
    assert _ids_secao("PARA OS CARGOS 15, 16 E 17") == {("CARGO", "15"), ("CARGO", "16"), ("CARGO", "17")}
    ls = [{"numero": 3}]
    m1, m2, m3 = {("", 3): (1, "C", "C")}, {("", 3): (2, "C", "C")}, {("", 3): (3, "C", "C")}
    enunc = {1: "O texto apresenta um roteiro.", 2: "O texto apresenta um roteiro.", 3: "A Lei 8.112 prevê..."}
    assert _mesmas_questoes(ls, [m1, m2], "", enunc) and not _mesmas_questoes(ls, [m1, m3], "", enunc)


def test_ocr_gabarito():
    from cebraspe_bank.extract.gabarito import _letra, _numera_por_posicao
    assert _letra("Cc", ocr=True) == "C" and _letra("XxX", ocr=True) == "X" and _letra("[o", ocr=True) is None
    assert _letra("EE") is None                           # PDF de texto: duas células coladas, não uma resposta
    # linha "Questão 41 42 ... " lida pelo OCR com '411', '7O' e 'rá'
    toks = ["Questão", "411", "42", "43", "7O", "rá", "46"]
    lw = [(0, 0, 30, 10, toks[0])] + [(50 + 25 * i, 0, 60 + 25 * i, 10, t) for i, t in enumerate(toks[1:])]
    nums = [w for w in lw if w[4].isdigit()]                # como em _linha_numeros: 411, 42, 43, 46
    assert [v for _, v in _numera_por_posicao(lw, nums, 25.0)] == [41, 42, 43, 44, 45, 46]
