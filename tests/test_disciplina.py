from cebraspe_bank import disciplina as D


def test_bloco():
    assert D.bloco("CONHECIMENTOS BÁSICOS") == "basicos"
    assert D.bloco("CONHECIMENTOS ESPECÍFICOS II") == "especificos"
    assert D.bloco("PROVA DISCURSIVA P2") == "discursiva"
    assert D.bloco("PROVA OBJETIVA P1") == "objetiva"
    assert D.bloco(None) is None
    assert D.bloco(None, "DISC") == "discursiva"


def test_assunto_literal():
    a, _ = D.assunto_de("CE", "item", "Acerca dos atos administrativos, julgue os itens a seguir.")
    assert a == "atos administrativos"
    a, _ = D.assunto_de("CE", "item", "Julgue os próximos itens, referentes a taxas de juros, custo efetivo e rendas.")
    assert a.startswith("taxas de juros")
    a, _ = D.assunto_de("ME", "A respeito do controle judicial dos atos administrativos, assinale a opção correta.", None)
    assert a == "controle judicial dos atos administrativos"
    a, _ = D.assunto_de("ME", "De acordo com o Código de Processo Civil, o pedido de gratuidade pode ser formulado", None)
    assert a == "Código de Processo Civil"


def test_referencias_nao_viram_assunto():
    for cmd in ("Com base nessa situação hipotética, julgue os itens a seguir.",
                "Considerando o texto CB1A1, julgue os itens.",
                "Com base no caso clínico hipotético precedente, julgue os itens seguintes.",
                "A respeito desse assunto, julgue os itens a seguir.",
                "A respeito do assunto apresentado no texto, julgue os itens a seguir.",
                "Considerando o conteúdo desse dispositivo, julgue os itens.",
                "Julgue os itens a seguir, relativos aos múltiplos aspectos a ele relacionados."):
        assert D.assunto_de("CE", "item", cmd)[0] is None, cmd


def test_lingua_portuguesa_pelo_trecho_literal():
    a, f = D.assunto_de("CE", "item", "Julgue os itens que se seguem, considerando as ideias, as propriedades "
                                      "linguísticas e o vocabulário do texto precedente.")
    assert D.disciplina_de("", "CONHECIMENTOS BÁSICOS", a, f) == ("Língua Portuguesa", "regra_assunto")


def test_precedencia_de_fontes():
    assert D.disciplina_de("LÍNGUA INGLESA", "CONHECIMENTOS BÁSICOS", "atos administrativos") == ("Língua Inglesa", "variante")
    assert D.disciplina_de("", "NOÇÕES DE INFORMÁTICA", "atos administrativos") == ("Noções de Informática", "titulo_pdf")
    assert D.disciplina_de("", "CONHECIMENTOS BÁSICOS", None, "Judge the following items.") == ("Língua Inglesa", "regra_comando")
    assert D.disciplina_de("", "CONHECIMENTOS ESPECÍFICOS", "conceitos") == (None, None)


def test_regras():
    casos = {
        "Lei n.º 8.112/1990": "Direito Administrativo",
        "Código de Processo Civil (CPC)": "Direito Processual Civil",
        "pronunciamentos técnicos do Comitê de Pronunciamentos Contábeis (CPC)": "Contabilidade",
        "CPC 46 (Mensuração do Valor Justo)": "Contabilidade",
        "Código de Ética Profissional do Servidor Público Civil do Poder Executivo Federal": "Ética no Serviço Público",
        "crimes ambientais": "Direito Ambiental",
        "prova no processo penal": "Direito Processual Penal",
        "bancos de dados relacionais e de linguagem SQL": "Tecnologia da Informação",
        "bibliotecas NumPy e Pandas": "Tecnologia da Informação",
        "formato MARC 21": "Biblioteconomia",
        "Código de Trânsito Brasileiro": "Legislação de Trânsito",
        "atuação do psicólogo em políticas públicas": "Psicologia",
    }
    for t, d in casos.items():
        assert D.disciplina_por_texto(t) == d, t
    # falsos positivos que as regras não podem pegar
    for t in ("sistema francês de amortização", "dívidas e suas causas", "vulnerabilidade socioambiental",
              "manual diagnóstico e estatístico de transtornos mentais", "elaboração de orçamentos de obras",
              "conceitos", "princípios"):
        assert D.disciplina_por_texto(t) is None, t
