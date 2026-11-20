from cebraspe_bank import edital as E
from cebraspe_bank.disciplina import combinar, nome_legivel

EDITAL = """
2.1 CARGO 1: ANALISTA
2.1.2 ÁREA 2
REQUISITO: diploma de conclusão de curso de graduação em Engenharia Civil, fornecido por instituição.
14 DOS OBJETOS DE AVALIAÇÃO (HABILIDADES E CONHECIMENTOS)
14.2 CONHECIMENTOS
14.2.2 CONHECIMENTOS BÁSICOS (PARA TODOS OS CARGOS)
LÍNGUA PORTUGUESA: 1 Compreensão e interpretação de textos de gêneros variados. 2 Reconhecimento de tipos
e gêneros textuais. 3 Domínio da ortografia oficial.
NOÇÕES DE DIREITO ADMINISTRATIVO: 1 Ato administrativo. 1.1 Conceito, requisitos e atributos. 2 Licitações e
contratos administrativos.
14.2.3 CONHECIMENTOS ESPECÍFICOS PARA O CARGO 1: ANALISTA
ÁREA 1
1 MACROECONOMIA. 1.1 Contabilidade Nacional. 1.2 Política monetária e fiscal. 2 MICROECONOMIA. 2.1 Teoria do
consumidor. 2.2 Estruturas de mercado.
ÁREA 2
1 Construção civil. 1.1 Planialtimetria. 2 Sistemas estruturais. 3 Geotecnia e fundações de edificações.
CARGO 2: ESPECIALISTA – ESPECIALIDADE 2
I
HIDROLOGIA:
1 Processos hidrológicos: precipitação, infiltração e escoamento superficial. 2 Hidrologia aplicada. II
HIDRÁULICA: 1 Condutos forçados e perdas de carga. III SISTEMAS HIDRÁULICOS DE SANEAMENTO: 1 Sistemas de
abastecimento de água. 2 Sistemas de coleta de esgotos: concepção e dimensionamento de sistemas coletores.
ANEXO I
"""


def _por_nome(ents):
    return {e["disciplina"]: e for e in ents}


def test_parse_formatos():
    ents = E.parse(EDITAL)
    d = _por_nome(ents)
    # "DISCIPLINA: 1 ..." no bloco de básicos, para todos os cargos
    assert d["LÍNGUA PORTUGUESA"]["bloco"] == "basicos" and d["LÍNGUA PORTUGUESA"]["cargos"] is None
    assert "Ato administrativo" in d["NOÇÕES DE DIREITO ADMINISTRATIVO"]["topicos"]
    # área sem "DISCIPLINA:": tópicos de 1º nível em maiúsculas viram disciplinas (ABIN)
    assert d["MACROECONOMIA"]["cargos"] == [1] and d["MACROECONOMIA"]["area"] == 1
    assert "Teoria do" in d["MICROECONOMIA"]["topicos"]
    # área só com tópicos: nome pelo curso do requisito
    assert d["ÁREA 2 – Engenharia Civil"]["tipo"] == "area"
    # romanos no meio da linha e nome quebrado (ANA); sem o prefixo "ESPECIALIDADE 2"
    for nome in ("HIDROLOGIA", "HIDRÁULICA", "SISTEMAS HIDRÁULICOS DE SANEAMENTO"):
        assert d[nome]["cargos"] == [2], nome


def test_cargos_e_rotulos():
    assert E._cargos("CARGOS 2 A 14: PERITO") == list(range(2, 15))
    assert E._cargos("CONHECIMENTOS BÁSICOS PARA OS CARGOS 1, 3 E 5") == [1, 3, 5]
    assert E._cargos("CONHECIMENTOS BÁSICOS (PARA TODOS OS CARGOS)") is None
    assert E.rotulo_area("PROVA OBJETIVA - ÁREA PROFISSIONAL: NUTRIÇÃO") == "NUTRIÇÃO"
    assert E.rotulo_area("CARGO 4: PERITO CRIMINAL FEDERAL – ÁREA 3: INFORMÁTICA FORENSE") == "INFORMÁTICA FORENSE"
    assert E.rotulo_area("PROVA OBJETIVA - CONHECIMENTOS ESPECÍFICOS - CARGO 2 - ÁREA 5") is None
    assert E.rotulo_generico("ADMINISTRATIVA") and E.rotulo_generico("Judiciária")
    assert not E.rotulo_generico("NUTRIÇÃO")
    assert E.cargo_area("CARGO 2 - ÁREA 5") == ({2}, 5)


def test_classificador():
    c = E.Classificador([{**e, "nome": e["disciplina"]} for e in E.parse(EDITAL)])
    # tópico quase literal decide entre disciplinas parecidas
    nome, fonte, _ = c.classificar("sistemas de coleta de esgotos", {2}, None, "especificos")
    assert (nome, fonte) == ("SISTEMAS HIDRÁULICOS DE SANEAMENTO", "edital_assunto")
    nome, fonte, _ = c.classificar("teoria do consumidor", {1}, 1, "especificos")
    assert (nome, fonte) == ("MICROECONOMIA", "edital_assunto")
    # área com uma só candidata
    assert c.classificar("qualquer coisa", {1}, 2, "especificos")[:2] == ("Engenharia Civil", "edital_unica")
    # questão de básicos só concorre com disciplinas de básicos
    nome, fonte, _ = c.classificar("atos administrativos e seus atributos", {1}, 1, "basicos")
    assert (nome, fonte) == ("NOÇÕES DE DIREITO ADMINISTRATIVO", "edital_assunto")
    # sem disciplina do mesmo grupo de bloco para o cargo: nada (não recai nas básicas)
    assert c.classificar("x", {9}, 7, "especificos")[1] in ("sem_candidata", "sem_assunto")


def test_precedencia():
    assert combinar("Língua Inglesa", "variante", "LÍNGUA PORTUGUESA", "edital_assunto") == ("Língua Inglesa", "variante")
    assert combinar("Direito Constitucional", "regra_assunto", "CONTABILIDADE", "edital_assunto") == \
        ("Contabilidade", "edital_assunto")
    assert combinar("Tecnologia da Informação", "regra_assunto", "INFORMÁTICA FORENSE", "edital_unica") == \
        ("Tecnologia da Informação", "regra_assunto")
    assert combinar(None, None, "NUTRIÇÃO", "area_prova") == ("Nutrição", "area_prova")
    assert combinar(None, None, "TRANSPORTES  AQUAVIÁRIOS", "edital_assunto") == ("Transportes Aquaviários", "edital_assunto")
    assert nome_legivel("ADMINISTRAÇÃO DE RECURSOS MATERIAIS") == "Administração de Recursos Materiais"
