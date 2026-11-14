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
