# Relatório final — banco de questões Cebraspe

Gerado em 2026-11-16T23:03:31+00:00 a partir de `cebraspe.db`.

## Visão geral

| Métrica | Valor |
|---|---|
| Concursos listados | 500 |
| Concursos com detalhe na API | 465 |
| Concursos com provas extraídas | 426 |
| Documentos baixados | 11154 (2.70 GB) |
| Provas processadas | 5205 |
| Provas com extração completa | 5103 (98.0%) |
| Provas parciais / falhas | 96 / 6 |

## Questões por tipo

| Tipo | Questões |
|---|---|
| CE | 156808 |
| ME | 53204 |
| DISC | 9514 |

### Itens de opção de língua estrangeira

| Variante | Questões | Com gabarito definitivo |
|---|---|---|
| LÍNGUA INGLESA | 45 | 45 |
| LÍNGUA ESPANHOLA | 45 | 45 |
| LÍNGUA FRANCESA | 10 | 10 |

## Gabaritos

Questões objetivas (C/E e ME) sem nenhum gabarito vinculado: **0** (0.0% de 210012). Cada caso tem pendência com o motivo.


Provas com **somente o gabarito preliminar** (definitivo não publicado ou não vinculado): **131** (9039 questões). Nelas `resposta_definitiva` fica vazia e a resposta está em `resposta_preliminar`; cada prova tem a pendência de validação correspondente.

| Com definitivo | Com preliminar | Anuladas | Alteradas | Com justificativa | Com padrão de resposta |
|---|---|---|---|---|---|
| 200973 | 26163 | 6127 | 1676 | 14446 | 6129 |

## Concursos e questões por ano

| Ano | Concursos | Provas | Questões |
|---|---|---|---|
|  | 1 | 0 | 0 |
| 2014 | 4 | 0 | 0 |
| 2015 | 35 | 66 | 3345 |
| 2016 | 21 | 320 | 13291 |
| 2017 | 31 | 252 | 12814 |
| 2018 | 37 | 445 | 21462 |
| 2019 | 24 | 184 | 11005 |
| 2020 | 28 | 285 | 14441 |
| 2021 | 59 | 486 | 21598 |
| 2022 | 52 | 438 | 17891 |
| 2023 | 57 | 718 | 27983 |
| 2024 | 47 | 1063 | 39954 |
| 2025 | 50 | 584 | 20823 |
| 2026 | 54 | 364 | 14919 |

## Fonte do ano do concurso

| ano_fonte | Concursos |
|---|---|
| edital_publicacao | 198 |
| edital_pdf | 146 |
| edital_nome | 109 |
| slug | 46 |
| (sem ano) | 1 |

## Pendências (abertas)

Lista completa em `data\pendencias.csv`.

| Etapa | Motivo (números agrupados) | Ocorrências |
|---|---|---|
| ano | concurso sem ano identificável | 6 |
| classificacao | prova inferida só pelo nome do arquivo | 23 |
| classificacao | gabarito sem fase clara (preliminar/definitivo) | 8 |
| classificacao | gabarito sem fase clara (preliminar/definitivo); sem código de prova no nome (vínculo depende do texto do PDF) | 1 |
| crawl | API detalhe HTTP N | 34 |
| crawl | concurso de teste publicado na API; ignorado | 1 |
| download | HTTP N | 10 |
| download | nome do arquivo corrompido na API (caractere inválido); URL irrecuperável | 7 |
| extracao | nenhuma questão segmentada | 6 |
| gabarito | padrão de resposta sem prova discursiva correspondente (N candidatas) | 337 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS – ÊNFASE N | GABARITO DEFINITIVO – CON | 20 |
| gabarito | nenhuma tabela de gabarito reconhecida no PDF | 16 |
| gabarito | justificativas: nenhuma linha de tabela reconhecida | 15 |
| gabarito | prova com gabarito embutido, mas nenhuma resposta reconhecida | 14 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N' sem prova correspondente | 14 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO PRELIMINAR – CONHECIMENTOS ESPECÍFICOS – DISCIPLINA N | GABARITO PRELIMINAR – | 12 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS – PERFIL I - TIPO N | GABARITO DEFINIT | 12 |
| gabarito | tabela vertical Questão/Gabarito (itens N–N) | 11 |
| gabarito | justificativas da seção 'None' sem prova correspondente | 10 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N – ÁREA N' sem prova correspondente | 8 |
| gabarito | fase no PDF (preliminar) difere da classificação (definitivo) | 6 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA OBJETIVA - CURSO DE FORMAÇÃO | GABARITO DEFINITIVO – CURSO | 6 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO PRELIMINAR - N.ª PROVA OBJETIVA - CURSO DE FORMAÇÃO | GABARITO PRELIMINAR - N | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS GERAIS PARA TODOS OS PERFIS - TIPO N | GABARITO DE | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS - PERFIL DE ASSISTENTE PCD - TIP | GAB | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS GERAIS PARA O PERFIL DE ASSISTENTE PCD - TIP | GAB | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CURSO DE FORMAÇÃO | GABARITO DEFINITIVO – CURSO DE FORMAÇÃO – Nª | 4 |
| gabarito | itens […] numerados pela posição (célula de número ilegível no PDF) | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS II – ESPECIALIDADE N – TARDE | GABARIT | 3 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N' sem prova correspondente | 3 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / QUÍMICA' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / FILOSOFIA' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / EIXO RECURSOS NATURAIS ‐ RN' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / EIXO PRODUÇÃO INDUSTRIAL ‐ PI' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / EIXO INFRAESTRUTURA ‐ IE' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / EIXO GESTÃO E NEGÓCIOS ‐ GN' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / EIXO AMBIENTE E SAÚDE ‐ AS' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS ARTE / CIÊNCIAS' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR' sem prova correspondente | 2 |
| gabarito | justificativas da seção 'HABILITAÇÃO N: LIBRAS' sem prova correspondente | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR' sem prova correspondente | 2 |
| gabarito | justificativas da seção 'CARGO: GUARDA CIVIL MUNICIPAL' ambíguas entre N provas | 2 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA DE VERIFICAÇÃO DE APRENDIZAGEM - CURSO DE FORMAÇÃO P | GAB | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS – BLOCO II – PARA OS CARGOS N, N E N / CARGO N: PERITO CRIMINAL FEDERAL – ÁREA N: ENGENHARIA  | 2 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – PERFIL N – UMA' ambíguas entre N p | 2 |
| gabarito | justificativas da seção 'Área Profissional: Saúde Coletiva – Programa: Multiprofissional em Atenção Básica' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'Área Profissional: Enfermagem – Programas: Multiprofissional em Atenção Básica e Atenção Cardíaca' sem prova corres | 1 |
| gabarito | justificativas da seção 'PRÉ‐REQUISITO EM PEDIATRIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS / Área: EDUCAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS / CARGO N: PROFESSOR ‐ ESPECIALIDADE: QUÍMICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL SUPERIOR' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: TÉCNICO MINISTERIAL' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: FARMÁCIA' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: SERVIÇO SOCIAL' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: ESTATÍSTICA' sem prova corresponde | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: PSICOLOGIA' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: DIREITO E LEGISLAÇÃO' sem prova co | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: ENGENHARIA ELÉTRICA' sem prova correspon | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: ENGENHARIA CIVIL' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: CONTABILIDADE' sem prova correspon | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: ENGENHARIA CIVIL' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: BIBLIOTECONOMIA' sem prova corresp | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: CONTÁBIL' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: CIÊNCIAS DA COMPUTAÇÃO' sem prova corres | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: ARQUIVOLOGIA' sem prova correspond | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: COMUNICAÇÃO SOCIAL' sem prova correspond | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: TÉCNICO DE ENFERMAGEM – URGÊNCIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: CIÊNCIAS CONTÁBEIS' sem prova correspond | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: BIBLIOTECONOMIA' sem prova correspondent | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: ANALISTA DE SISTEMA (DESENVOLVIMEN | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: ARQUITETURA' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: AUDITOR DE CONTROLE EXTERNO – ÁREA: FISCALIZAÇÃO – ESPECIALIDADE: ARQ | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: ADMINISTRAÇÃO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: ADMINISTRAÇÃO' sem prova correspon | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: ADMINISTRAÇÃO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: TÉCNICO JURÍDICO – ESPECIALIDADE: ELETRICIDADE E COMUNICAÇÃO' sem pro | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: TÉCNICO JURÍDICO – ESPECIALIDADE: APOIO ADMINISTRATIVO' sem prova cor | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: OFICIAL DE JUSTIÇA AVALIADOR' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: PSICOLOGIA' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: JORNALISMO' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: TÉCNICO DESPOR | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ENGENHEIRO DE  | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ENGENHEIRO/ÁRE | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: EDITOR DE PUBL | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ASSISTENTE SOC | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ASSISTENTE EM  | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE NÍVEL MÉDIO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROGRAMAS DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES EM ÁREA DE ATUAÇÃO COM EXIGÊNCIA DE PRÉ‐ REQUISITO EM RADIOLOGIA E | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES COM EXIGÊNCIA DE PRÉ-REQUISITO EM CLÍNICA MÉDICA – PROGRAMAS: CANCE | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES COM EXIGÊNCIA DE PRÉ-REQUISITO EM CIRURGIA- GERAL – PROGRAMAS: CIRU | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES COM EXIGÊNCIA DE PRÉ-REQUISITO EM CIRURGIA- GERAL OU OBSTETRÍCIA E  | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA DE ACESSO DIRETO – PROGRAMAS: ANESTESIOLOGIA / CIRURGIA-GERAL / CIRURGIA GERAL - ÁREA | 1 |
| gabarito | justificativas da seção 'FUNÇÃO N: JUIZ LEIGO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'FUNÇÃO N: CONCILIADOR' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'ESTÁGIO REMUNERADO DE PÓS-GRADUAÇÃO EM DIREITO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: UROLOGIA' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS ÁREAS DE ATUAÇÃO / ÁREA DE ATUAÇÃO N: MATEMÁTICA E ÁREAS AFINS' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS ÁREAS DE ATUAÇÃO / ÁREA DE ATUAÇÃO N: LETRAS, LINGUÍSTICA E ÁREAS DE LÍNGUA INGL | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS – ESPECIALIDADE N: TECNOLOGIA DA INFORMAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS ‐ PROGRAMA MULTIPROFISSIONAL EM ATENÇÃO BÁSICA ‐ ÁREA PROFISSIONAL: ODONTOLOGIA E PROGRAM | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS - PROGRAMA MULTIPROFISSIONAL EM ATENÇÃO BÁSICA - ÁREA PROFISSIONAL: SAÚDE COLETIVA' sem p | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS - PROGRAMA MULTIPROFISSIONAL EM ATENÇÃO BÁSICA - ÁREA PROFISSIONAL: ENFERMAGEM' sem prova | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECIFÍCOS GRUPO II - DISCIPLINA: BIOLOGIA / GRUPO II - DISCIPLINA: LÍNGUA PORTUGUESA' ambíguas entr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS COMPLEMENTARES PARA OS CARGOS N, N E N / CARGO N: PESQUISADOR EM PROPRIEDADE INDUSTRIAL – ÁREA DE CON | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS – BLOCO II – PARA OS CARGOS N, N E N / CARGO N: PERITO CRIMINAL FEDERAL – ÁREA N: INFORMÁTICA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM REGULAÇÃO DE AVIAÇÃO CIVIL – ÁREA N' ambíguas | 1 |
| gabarito | justificativas da seção 'CARGOS DE ESPECIALISTA EM REGULAÇÃO E VIGILÂNCIA SANITÁRIA' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO: NEONATOLOGIA – ITENS N E N' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO: ESPECIALISTA EM REGULAÇÃO E VIGILÂNCIA SANITÁRIA – ÁREA N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO: ESPECIALISTA EM FINANCIAMENTO E EXECUÇÃO DE PROGRAMAS E PROJETOS EDUCACIONAIS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO: ESPECIALISTA EM FINANCIAMENTO E EXECUÇÃO DE PROGRAMAS E PROJETOS EDUCACIONAIS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO: DEFENSOR PÚBLICO SUBSTITUTO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO: AUDITOR (CONSELHEIRO-SUBSTITUTO) DO TRIBUNAL DE CONTAS DO DISTRITO FEDERAL GABARITO' sem prova correspondent | 1 |
| gabarito | justificativas da seção 'CARGO DE PROCURADOR DE CONTAS SUBSTITUTO DO MINISTÉRIO PÚBLICO DE CONTAS DO MPC/MS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO DE ESPECIALISTA EM REGULAÇÃO DE SAÚDE SUPLEMENTAR' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO DE DEFENSOR PÚBLICO DO ESTADO DE NÍVEL I' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE PREVIDÊNCIA COMPLEMENTAR – ÁREA N: JURÍDICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE PREVIDÊNCIA COMPLEMENTAR – ÁREA N: GESTÃO DE INVESTIMENTOS E RISCOS DE INVESTIMENTOS' ambíguas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA PORTUÁRIO II – ÁREA: CONTRATOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: DELEGADO DE POLÍCIA CIVIL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPECIALIDADE: ANÁLISE DE SISTEMAS' sem prova correspond | 1 |
| gabarito | justificativas da seção 'CARGO N: SOLDADO COMBATENTE' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: DATILOSCOPISTA POLICIAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE PREVIDÊNCIA COMPLEMENTAR – ÁREA N: GOVERNANÇA, AUDITORIA, CONTROLE E CONFORMIDADE' ambíguas en | 1 |
| gabarito | justificativas da seção 'CARGO N' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: TÉCNICO BANCÁRIO III – ÁREA: INFORMÁTICA – ESPECIALIDADE: DESENVOLVIMENTO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: OFICIAL COMBATENTE' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: AUXILIAR DE LEGISTA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA ADMINISTRATIVO DE CONTROLE EXTERNO – ÁREA DE GESTÃO – ESPECIALIDADE SERVIÇOS TÉCNICOS E ADMINISTR | 1 |
| gabarito | justificativas da seção 'CN - CONHECIMENTOS COMPLEMENTARES PARA AS OPÇÕES N, N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CN - CONHECIMENTOS COMPLEMENTARES PARA A OPÇÃO N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – UINFRA (ENGENHARIA E ARQUITETURA)  | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – PERFIL N – USI' ambíguas entre N p | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – PERFIL N – UDIGIS' ambíguas entre  | 1 |
| gabarito | justificativas da seção 'BLOCO I - CBN / PROVA DE CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL MÉDIO' sem prova correspondente | 1 |
| gabarito | gabarito lido da imagem da página N (OCR por célula) | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – PROGRAMA DE CAPACITAÇÃO (PROCAP) | GABARITO DEFINITIVO – PROGRAM | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CURSO DE FORMAÇÃO – Nª TURMA | GABARITO DEFINITIVO – CURSO DE FO | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS – CARGO N | GABARITO DEFINITIVO – CONH | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA OBJETIVA - CURSO DE FORMAÇÃO | GABARITO DEFINITIVO – PROVA | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA OBJETIVA - CURSO DE FORMAÇÃO (Nª TURMA) | GABARITO DEFINIT | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CURSO DE PREPARAÇÃO - N/N/N | GABARITO DEFINITIVO - CURSO DE PRE | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CURSO DE FORMAÇÃO - Nª TURMA | GABARITO DEFINITIVO – PROVA OBJET | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CURSO DE FORMAÇÃO - Nª TURMA | GABARITO DEFINITIVO – CURSO DE FO | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS ESPECÍFICOS - CARGO N | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS ESPECÍFICOS - CARGO N | GABARITO DEFINITIVO - CONH | 1 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS ESPECÍFICOS - ATIVIDADE N | GABARITO DEFINITIVO -  | 1 |
| validacao | somente gabarito preliminar (definitivo não publicado ou não vinculado) | 131 |
| validacao | prova sem gabarito vinculado | 90 |
| validacao | nº de itens extraídos (N) difere do gabarito (N) | 6 |

## Observações de método

- Nada é estimado: resposta, ano ou texto que não pôde ser lido fica NULL e gera pendência.
- `alterada=1` só quando há evidência (preliminar e definitivo publicados, ou tabela de justificativas). O site costuma retirar o gabarito preliminar após o definitivo, então a ausência de alteração não é prova de que o item não mudou.
- Itens de opção de língua estrangeira (ex.: itens 1–10 em espanhol e em inglês) são guardados por língua (`questao.variante`, `gabarito_bruto.variante`): na prova pelo título 'LÍNGUA X' de cada bloco e no gabarito pela cor da célula e a legenda. Conflitos que a legenda não resolve ficam sem resposta.
- Versões de acessibilidade (adaptada, superampliada, ledor, braile, VLibras) foram ignoradas.
- Números de itens ofuscados (substituição de glifos, comum em 2015–2017) são decodificados pela restrição de sequência consecutiva.


### Concursos sem detalhe na API

`ANATEL_14`, `ANTAQ_14`, `DEPEN_15`, `DPE_PE_14_DEFENSOR`, `DPE_RN_15_DEFENSOR`, `DPF_14_AGENTE`, `DPU_15_ADMINISTRATIVO`, `FUB_15_1`, `FUNPRESP_15`, `MEC_15_TEMPORARIO`, `MPU_15`, `MP_15_ENAP`, `PREF_SALVADOR_15_PROCURADOR`, `SEC_BA_15_DIRETOR_E_VICE`, `SES_DF_15_MULTIPROFISSIONAL`, `SES_DF_15_MULTIPROFISSIONAL_2`, `SES_DF_15_RESIDENCIA`, `SES_DF_16_MULTIPROFISSIONAL`, `SES_DF_16_RESIDENCIA`, `STJ_15`, `TCE_PR_15_AUDITOR`, `TCE_RN_15_SERVIDOR`, `TCE_SC_15`, `TC_RN_15_AUDITOR`, `TELEBRAS_15`, `TESTE_2029`, `TJDFT_15_JUIZ`, `TJDFT_15_JUIZ_2`, `TJ_AM_15_JUIZ`, `TJ_PB_15_JUIZ`, `TRE_MT_15`, `TRE_PE_15`, `TRE_PI_15`, `TRE_RS_15`, `TRF1_15_JUIZ`
