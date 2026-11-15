# Relatório final — banco de questões Cebraspe

Gerado em 2026-11-15T11:29:47+00:00 a partir de `cebraspe.db`.

## Visão geral

| Métrica | Valor |
|---|---|
| Concursos listados | 500 |
| Concursos com detalhe na API | 465 |
| Concursos com provas extraídas | 426 |
| Documentos baixados | 11152 (2.70 GB) |
| Provas processadas | 5212 |
| Provas com extração completa | 5026 (96.4%) |
| Provas parciais / falhas | 167 / 19 |

## Questões por tipo

| Tipo | Questões |
|---|---|
| CE | 156791 |
| ME | 53204 |
| DISC | 9490 |

### Itens de opção de língua estrangeira

| Variante | Questões | Com gabarito definitivo |
|---|---|---|
| LÍNGUA INGLESA | 45 | 45 |
| LÍNGUA ESPANHOLA | 45 | 45 |
| LÍNGUA FRANCESA | 10 | 10 |

## Gabaritos

Questões objetivas (C/E e ME) sem nenhum gabarito vinculado: **1049** (0.5% de 209995). Cada caso tem pendência com o motivo.

| Com definitivo | Com preliminar | Anuladas | Alteradas | Com justificativa | Com padrão de resposta |
|---|---|---|---|---|---|
| 199895 | 23536 | 6064 | 1501 | 13756 | 6123 |

## Concursos e questões por ano

| Ano | Concursos | Provas | Questões |
|---|---|---|---|
|  | 1 | 0 | 0 |
| 2014 | 4 | 0 | 0 |
| 2015 | 35 | 66 | 3345 |
| 2016 | 21 | 324 | 13302 |
| 2017 | 31 | 254 | 12814 |
| 2018 | 37 | 445 | 21462 |
| 2019 | 24 | 184 | 11005 |
| 2020 | 28 | 285 | 14396 |
| 2021 | 59 | 486 | 21595 |
| 2022 | 52 | 438 | 17889 |
| 2023 | 57 | 718 | 27983 |
| 2024 | 47 | 1063 | 39951 |
| 2025 | 50 | 584 | 20823 |
| 2026 | 54 | 365 | 14920 |

## Fonte do ano do concurso

| ano_fonte | Concursos |
|---|---|
| edital_publicacao | 198 |
| edital_pdf | 146 |
| edital_nome | 109 |
| slug | 46 |
| (sem ano) | 1 |

## Pendências (abertas)

Lista completa em `data/pendencias.csv`.

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
| extracao | nenhuma questão segmentada | 19 |
| gabarito | padrão de resposta sem prova discursiva correspondente (N candidatas) | 340 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS – ÊNFASE N | GABARITO DEFINITIVO – CON | 20 |
| gabarito | prova com gabarito embutido, mas nenhuma resposta reconhecida | 19 |
| gabarito | nenhuma tabela de gabarito reconhecida no PDF | 17 |
| gabarito | justificativas: nenhuma linha de tabela reconhecida | 15 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N' sem prova correspondente | 14 |
| gabarito | justificativas da seção 'None' sem prova correspondente | 12 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO PRELIMINAR – CONHECIMENTOS ESPECÍFICOS – DISCIPLINA N | GABARITO PRELIMINAR – | 12 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIAS AGRÁRIAS  | 12 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS BÁSICOS PARA O CARGO DE MONITOR DE GESTÃO EDUCACIONAL / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSI | 9 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE NÍVEL MÉDIO / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZAD | 9 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N – ÁREA N' sem prova correspondente | 8 |
| gabarito | fase no PDF (preliminar) difere da classificação (definitivo) | 6 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA OBJETIVA - CURSO DE FORMAÇÃO | GABARITO DEFINITIVO – CURSO | 6 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL MÉDIO / CARGO N: ANALISTA MINISTERIAL ESPECIALIZADO – ÁREA DE AT | 6 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIAS EXATAS E  | 5 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: AUDITOR EM SAÚDE – | 5 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO PRELIMINAR - N.ª PROVA OBJETIVA - CURSO DE FORMAÇÃO | GABARITO PRELIMINAR - N | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS GERAIS PARA TODOS OS PERFIS - TIPO N | GABARITO DE | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS - PERFIL DE ASSISTENTE PCD - TIP | GAB | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS GERAIS PARA O PERFIL DE ASSISTENTE PCD - TIP | GAB | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CURSO DE FORMAÇÃO | GABARITO DEFINITIVO – CURSO DE FORMAÇÃO – Nª | 4 |
| gabarito | justificativas da seção 'TIPO N PERFIL II: ANALISTA TÉCNICO II – EDUCAÇÃO' ambíguas entre N provas | 4 |
| gabarito | justificativas da seção 'TIPO N PERFIL N: ANALISTA TÉCNICO II – AUDITORIA INTERNA' ambíguas entre N provas | 4 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIAS BIOLÓGICA | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO (MODELO) – CONHECIMENTOS ESPECÍFICOS – CARGO N | GABARITO DEFINITI | 4 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO – CONHECIMENTOS ESPECÍFICOS II – ESPECIALIDADE N – TARDE | GABARIT | 3 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS BÁSICOS PARA O CARGO DE NÍVEL MÉDIO | GABARITO DEF | 3 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: NEURO | 3 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: MEDIC | 3 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / CN - CONHECIMENTOS COMPLEMENTARES PARA A OPÇÃO  | 3 |
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
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS SOMENTE PARA O CARGO N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPECIALI | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR' sem prova correspondente | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPECIALIDADE: CO | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPECIALIDADE: AR | 2 |
| gabarito | justificativas da seção 'CARGO: GUARDA CIVIL MUNICIPAL' ambíguas entre N provas | 2 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA OBJETIVA PN | GABARITO DEFINITIVO - PROVA OBJETIVA PN | 2 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - PROVA DE VERIFICAÇÃO DE APRENDIZAGEM - CURSO DE FORMAÇÃO P | GAB | 2 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: CANCE | 2 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: FISIOTERAPEUTA – ÁREA: TERAPIA INTE | 2 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS BÁSICOS PARA O CARGO DE MONITOR DE GESTÃO EDUCACIONAL / CARGO N – ANALISTA DE GESTÃO EDUCAC | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA OS CARGOS N E N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPE | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS – BLOCO II – PARA OS CARGOS N, N E N / CARGO N: PERITO CRIMINAL FEDERAL – ÁREA N: ENGENHARIA  | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM GESTÃO DE TELECOMUNICAÇÕES – ANALISTA SUPERIO | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS PERFIS N E N' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS EMPREGOS N E N' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL UNIVERSITÁRIO JUNIOR – FUNÇÃO: ANALI | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPECIALIDA | 2 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O PERFIL N' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'CN - CONHECIMENTOS COMPLEMENTARES PARA A OPÇÃO N' ambíguas entre N provas | 2 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – PERFIL N – UMA' ambíguas entre N p | 2 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – UGP' ambíguas entre N provas | 2 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS ESPECÍFICOS – CARGO N | GABARITO DEFINITIVO - CONH | 2 |
| gabarito | gabarito ambíguo para a prova (respostas diferentes): GABARITO DEFINITIVO - CONHECIMENTOS BÁSICOS (PROVA OBJETIVA PN) - CARGO N | GABARITO D | 2 |
| gabarito | tabela não confiável: N itens com respostas conflitantes; descartada | 1 |
| gabarito | justificativas da seção 'Área Profissional: Saúde Coletiva – Programa: Multiprofissional em Atenção Básica' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'Área Profissional: Enfermagem – Programas: Multiprofissional em Atenção Básica e Atenção Cardíaca' sem prova corres | 1 |
| gabarito | justificativas da seção 'PRÉ‐REQUISITO EM PEDIATRIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: ULTRA | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: REUMA | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: PSIQU | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: ORTOP | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: NEONA | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: HEMAT | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: GERIA | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: GASTR | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: ANGIO | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: ENDOC | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: ANEST | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: CIRUR | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: CARDIOLOGIA' amb | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ANALISTA ADMINISTRATIVO – ESPECIALI | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: FONOAUDIÓLOGO' ambíguas entre N pro | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: FÍSICO – ÁREA: FÍSICA MÉDICA – ESPE | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: FARMACÊUTICO' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: BIÓLOGO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: TERAPIA INTENSIV | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: SAÚDE MENTAL' am | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: SAÚDE INDÍGENA'  | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: SAÚDE DA CRIANÇA | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ASSISTENTE SOCIAL' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ADVOGADO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: ONCOLOGIA' ambíg | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – HEMATOLOGIA E HEMOTERA | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: DERMATOLÓGICA –  | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENFERMEIRO – ÁREA: CARDIOLOGIA – ES | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS / Área: EDUCAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS / CARGO N: PROFESSOR ‐ ESPECIALIDADE: GEOGRAFIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS ESPECÍFICOS / CARGO N: PROFESSOR ‐ ESPECIALIDADE: QUÍMICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVAS DE CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL SUPERIOR' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA OBJETIVA (PN) - CONHECIMENTOS ESPECÍFICOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR (EXCETO PARA CARGOS N, N, N)' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS GERAIS / CARGO N: OFICIAL TÉCNICO DE INTELIGÊNCIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGOS DE N A N: PROFESSOR DE EDUCAÇÃO BÁSICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: TÉCNICO MINISTERIAL' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: FARMÁCIA' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: PSICOLOGIA' ambíguas entre N pro | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: SERVIÇO SOCIAL' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: ESTATÍSTICA' sem prova corresponde | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: PSICOLOGIA' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: DIREITO E LEGISLAÇÃO' sem prova co | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA DE CONTROLE – ÁREA: ENGENHARIA ELÉTRICA' sem prova correspon | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA MINISTERIAL – ÁREA: ENGENHARIA CIVIL' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: CONTABILIDADE' sem prova correspon | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: DIREITO' ambíguas entre N provas | 1 |
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
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: AUXILIAR JUDICIÁRIO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: OFICIAL DE JUSTIÇA AVALIADOR' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: PSICOLOGIA' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA JURÍDICO – ESPECIALIDADE: JORNALISMO' sem prova corresponden | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: TÉCNICO DESPOR | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ENGENHEIRO DE  | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ENGENHEIRO/ÁRE | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: EDITOR DE PUBL | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ASSISTENTE SOC | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: TÉCNICO EM SEG | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: TÉCNICO DE TEC | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS/ÁREAS DE NÍVEL MÉDIO (EXCETO CARGO N) / CARGO N: ASSISTENTE EM  | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS DE NÍVEL MÉDIO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – EDUCAÇÃO INFANTIL E E | 1 |
| gabarito | justificativas da seção 'PROVA DE CONHECIMENTOS BÁSICOS PARA OS CARGOS DE PERITO CRIMINAL FEDERAL (TODAS AS ÁREAS) / CARGO N: PERITO CRIMINA | 1 |
| gabarito | justificativas da seção 'PROGRAMAS DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES EM ÁREA DE ATUAÇÃO COM EXIGÊNCIA DE PRÉ‐ REQUISITO EM RADIOLOGIA E | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES COM EXIGÊNCIA DE PRÉ-REQUISITO EM CLÍNICA MÉDICA – PROGRAMAS: CANCE | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES COM EXIGÊNCIA DE PRÉ-REQUISITO EM CIRURGIA- GERAL – PROGRAMAS: CIRU | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA EM ESPECIALIDADES COM EXIGÊNCIA DE PRÉ-REQUISITO EM CIRURGIA- GERAL OU OBSTETRÍCIA E  | 1 |
| gabarito | justificativas da seção 'PROGRAMA DE RESIDÊNCIA MÉDICA DE ACESSO DIRETO – PROGRAMAS: ANESTESIOLOGIA / CIRURGIA-GERAL / CIRURGIA GERAL - ÁREA | 1 |
| gabarito | justificativas da seção 'PERFIL III: ANALISTA TÉCNICO II – ARQUIVOLOGIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'PERFIL N: ANALISTA TÉCNICO II – UNIVERSIDADE CORPORATIVA SEBRAE' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: DIREITO E AUDITORIA – SUBÁREA: AUDITORIA CONTÁBIL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: SUPRIMENTO, MANUTENÇÃO E SERVIÇOS – SUBÁREA: ATIVOS PATRIMONIAIS E IMOBILIÁRIOS' ambíguas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: TRANSFERÊNCIA DE TECNOLOGIA E COMUNICAÇÃO – SUBÁREA: GESTÃO DE INSTRUMENTOS DE PARCERIAS  | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: SUPRIMENTO, MANUTENÇÃO E SERVIÇOS – SUBÁREA: INFRAESTRUTURA – ENGENHARIA CIVIL' ambíguas  | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: SUPRIMENTO, MANUTENÇÃO E SERVIÇOS – SUBÁREA: INFRAESTRUTURA – ARQUITETURA' ambíguas entre | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS AGRÁRIAS – SUBÁREA: CLÍNICA VETERINÁRIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS BIOLÓGICAS – SUBÁREA: BIOLOGIA MOLECULAR E GENÉTICA ANIMAL' ambíguas entre N pro | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: SUPRIMENTO, MANUTENÇÃO E SERVIÇOS – SUBÁREA: INFRAESTRUTURA – ENGENHARIA ELÉTRICA' ambígu | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO ESTRATÉGICA – SUBÁREA: ARTICULAÇÃO POLÍTICO-INSTITUCIONAL NACIONAL' ambíguas entre | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO ESTRATÉGICA – SUBÁREA: ARTICULAÇÃO POLÍTICO-INSTITUCIONAL INTERNACIONAL' ambíguas  | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS EXATAS E DA TERRA – SUBÁREA: SISTEMAS DE INFORMAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO DE PESSOAS – SUBÁREA: FOLHA DE PAGAMENTO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: SUPRIMENTO, MANUTENÇÃO E SERVIÇOS – SUBÁREA: ADMINISTRATIVO, SUPRIMENTO, MANUTENÇÃO E SER | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: ORÇAMENTO E FINANÇAS – SUBÁREA: CONTABILIDADE' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO DA INFORMAÇÃO – SUBÁREA: ENGENHARIA DE DADOS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS BIOLÓGICAS – SUBÁREA: BIOLOGIA AVANÇADA E TECNOLOGIA DA INFORMAÇÃO' ambíguas ent | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS BIOLÓGICAS – SUBÁREA: BIOLOGIA AVANÇADA E BIOINFORMÁTICA' ambíguas entre N prova | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS EXATAS E DA TERRA – SUBÁREA: AGRICULTURA E CLIMATOLOGIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS AGRÁRIAS – SUBÁREA: RECURSOS GENÉTICOS MICROBIANOS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS AGRÁRIAS – SUBÁREA: RECURSOS PESQUEIROS E ENGENHARIA DE PESCA' ambíguas entre N  | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: TRANSFERÊNCIA DE TECNOLOGIA E COMUNICAÇÃO – SUBÁREA: INOVAÇÃO SOCIAL' ambíguas entre N pr | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS BIOLÓGICAS – SUBÁREA: BIOLOGIA AVANÇADA E QUÍMICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: LABORATÓRIOS E CAMPOS EXPERIMENTAIS – SUBÁREA: LABORATÓRIO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO DA INFORMAÇÃO – SUBÁREA: GESTÃO DA INFORMAÇÃO EDIÇÃO – INGLÊS/PORTUGUÊS' ambíguas  | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO DA INFORMAÇÃO – SUBÁREA: ENGENHARIA DE SOFTWARE' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS AGRÁRIAS – SUBÁREA: TECNOLOGIA DE SEMENTES' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS BIOLÓGICAS – SUBÁREA: INSUMOS BIOLÓGICOS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO DA INFORMAÇÃO – SUBÁREA: GESTÃO DA INFORMAÇÃO E DA PROGRAMAÇÃO – TEXTOS TÉCNICO-CI | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: CIÊNCIAS AGRÁRIAS – SUBÁREA: SISTEMA DE PRODUÇÃO VEGETAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: TRANSFERÊNCIA DE TECNOLOGIA E COMUNICAÇÃO – SUBÁREA: COMUNICAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO ESTRATÉGICA – SUBÁREA: GOVERNANÇA SUSTENTÁVEL – ESG' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: NANOTECNOLOGIA – SUBÁREA: NANOTECNOLOGIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: LABORATÓRIOS E CAMPOS EXPERIMENTAIS – SUBÁREA: APOIO A CAMPO EXPERIMENTAL' ambíguas entre | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: LABORATÓRIOS E CAMPOS EXPERIMENTAIS – SUBÁREA: CULTURA DE TECIDOS' ambíguas entre N prova | 1 |
| gabarito | justificativas da seção 'OPÇÃO N: ANALISTA – ÁREA: GESTÃO DE PESSOAS – SUBÁREA: SAÚDE OCUPACIONAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'FUNÇÃO N: JUIZ LEIGO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'FUNÇÃO N: CONCILIADOR' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'ESTÁGIO REMUNERADO DE PÓS-GRADUAÇÃO EM DIREITO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'Cargo N: AUDITOR DE CONTROLE EXTERNO – ESPECIALIDADE: ECONOMIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS PEDAGÓGICOS PARA TODOS OS CARGOS / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – ÁREA DE ATUAÇÃO: GRUPO I – | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA OS CARGOS N A N / CARGO N: ANALISTA ADMINISTRATIVO – ESPECIALIDADE: ENGENHARIA EL | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA OS CARGOS N A N / CARGO N: ANALISTA ADMINISTRATIVO – ESPECIALIDADE: DIREITO' ambí | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA OS CARGOS N A N / CARGO N: ANALISTA ADMINISTRATIVO – ESPECIALIDADE: ADMINISTRAÇÃO | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA OS CARGOS N A N / CARGO N: ESPECIALISTA EM RECURSOS MINERAIS – ESPECIALIDADE: DIR | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA OS CARGOS N A N / CARGO N: ANALISTA ADMINISTRATIVO – ESPECIALIDADE: QUALQUER ÁREA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA O EMPREGO N / EMPREGO N: ANALISTA – ESPECIALIDADE: SEGURIDADE' ambíguas entre N p | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA O CARGO N / CARGO N: ANALISTA DE GESTÃO EDUCACIONAL – ESPECIALIDADE: FONOAUDIOLOG | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS SOMENTE PARA O CARGO N / CARGO N: ANALISTA DE GESTÃO EDUCACIONAL – ESPECIALIDADE: CIÊNCIAS CON | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS/AS ÁREAS / ÁREA N: ANALISTA – GESTÃO CORPORATIVA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: NUTRICIONISTA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: UROLOGIA' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: OBSTETRÍCIA' ambígua | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: NEUROPEDIATRIA' ambí | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: NEONATALOGIA' ambígu | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: GINECOLOGIA' ambígua | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: ENDOSCOPIA' ambíguas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: CIRURGIA VASCULAR' a | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: CIRURGIA CARDÍACA' a | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS DE NÍVEL SUPERIOR / CARGO N: MÉDICO – ESPECIALIDADE: CARDIOPEDIATRIA' amb | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: COMUNICADOR SOCIAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: ANALISTA JUDICIÁRIO – GRUPO: NÍVEL SUPERIOR – SEM ESPECIALIDAD | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: ANALISTA DE PLANEJAMENTO E ORÇAMENTO – ESPECIALIDADE: GESTÃO D | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: ANALISTA – ESPECIALIDADE: ENGENHEIRO AMBIENTAL' ambíguas entre | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: ANALISTA DE CONTROLE EXTERNO – ESPECIALIDADE: CIÊNCIAS CONTÁBE | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: AGENTE DE POLÍCIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / CARGO N: ANALISTA JUDICIÁRIO – GRUPO: TECNOLOGIA DA INFORMAÇÃO – ESPECI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / ATIVIDADE N: ATIVIDADES DE REGULAÇÃO DE NOVAS ATRIBUIÇÕES IV' ambíguas  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / ATIVIDADE N: ATIVIDADES DE REGULAÇÃO DE NOVAS ATRIBUIÇÕES III' ambíguas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / ATIVIDADE N: ATIVIDADES DE REGULAÇÃO DE NOVAS ATRIBUIÇÕES II' ambíguas  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / ATIVIDADE N: ATIVIDADES DE REGULAÇÃO DE NOVAS ATRIBUIÇÕES I' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODOS OS CARGOS / ATIVIDADE N: ATIVIDADES DE FISCALIZAÇÃO DE INFRAESTRUTURA E MOVIMENTAÇÃ | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS ÁREAS DE ATUAÇÃO / ÁREA DE ATUAÇÃO N: MATEMÁTICA E ÁREAS AFINS' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS ÁREAS DE ATUAÇÃO / ÁREA DE ATUAÇÃO N: LETRAS, LINGUÍSTICA E ÁREAS DE LÍNGUA INGL | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE TÉCNICO / OPÇÃO N: TÉCNICO – ÁREA: MECÂNICA – SUBÁREA: MECÂNI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE TÉCNICO / OPÇÃO N: TÉCNICO – ÁREA: TRANSFERÊNCIA DE TECNOLOGI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE TÉCNICO / OPÇÃO N: TÉCNICO – ÁREA: SUPRIMENTO, MANUTENÇÃO E S | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE TÉCNICO / OPÇÃO N: TÉCNICO – ÁREA: LABORATÓRIO E CAMPOS EXPER | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE TÉCNICO / OPÇÃO N: ASSISTENTE – ÁREA: SUPRIMENTO, MANUTENÇÃO  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: TRANSFERÊNCIA DE T | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: ENGENHARIAS – SUBÁ | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIAS AMBIENTAI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIA E TECNOLOG | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: ESPECTROSCOPIA APL | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIAS DA SAÚDE  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA TODAS AS OPÇÕES DO CARGO DE PESQUISADOR / OPÇÃO N: PESQUISADOR – ÁREA: CIÊNCIAS SOCIAIS A | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: AUDITOR DE SAÚDE – | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: PROFISSIONAL DE ED | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: MÉDICO ORTOPEDISTA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: MÉDICO OFTALMOLOGI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: MÉDICO CLÍNICO GER | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: MÉDICO AUDITOR' am | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: FONOAUDIÓLOGO' amb | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR, EXCETO PARA OS CARGOS N, N E N / CARGO N: ENGENHEIRO ELETRIC | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ARQUITETO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: TÉCNICO EM GEOPROCESSAMENTO' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: ENGENHEIRO DE SEGURANÇA DO TRABALHO' ambíguas entr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE NÍVEL SUPERIOR / CARGO N: JORNALISTA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE ANALISTA LEGISLATIVO, EXCETO PARA AS ÁREAS: CONSULTORIA TÉCNICA LEGISLATIVA, | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: MÉDICO – ESPECIALIDADE: DERMATOLOGISTA' ambíguas entre N pr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PSICÓLOGO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PROFESSOR – DISCIPLINA: MATEMÁTICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PROFESSOR – DISCIPLINA: LÍNGUA PORTUGUESA' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PROFESSOR – DISCIPLINA: LÍNGUA INGLESA' ambíguas entre N pr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PROFESSOR – DISCIPLINA: GEOGRAFIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PROFESSOR – DISCIPLINA: EDUCAÇÃO FÍSICA' ambíguas entre N p | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: PROFESSOR – DISCIPLINA: CIÊNCIAS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: MÉDICO – ESPECIALIDADE: SOCORRISTA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: MÉDICO – ESPECIALIDADE: PNEUMOLOGISTA' ambíguas entre N pro | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: MÉDICO – ESPECIALIDADE: NEUROLOGISTA' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: MÉDICO – ESPECIALIDADE: INFECTOLOGISTA' ambíguas entre N pr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N / CARGO N: MÉDICO – ESPECIALIDADE: GASTROENTEROLOGISTA INFANTIL' ambíg | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS DE N A N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N, N, N, N E N / CARGO N: AUDITOR DE CONTROLE EXTERNO – ESPECIALIDADE: TECNOLOG | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: FISIOTERAPEUTA' ambíguas entre N pro | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: FARMACÊUTICO' ambíguas entre N prova | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: ESPECIALISTA EM EPIDEMIOLOGIA E VIGI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: ENFERMEIRO INTENSIVISTA PEDIÁTRICO'  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ASSISTENTE TÉCNICO – ESPECIALIDADE: TÉCNICO EM SAÚDE BUCAL' am | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ASSISTENTE TÉCNICO – ESPECIALIDADE: TÉCNICO EM RADIOLOGIA' amb | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ASSISTENTE TÉCNICO – ESPECIALIDADE: TÉCNICO EM IMOBILIZAÇÃO OR | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: MÉDICO – ESPECIALIDADE: ULTRASSONOGRAFISTA' ambíguas entre N p | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: ASSISTENTE SOCIAL' ambíguas entre N  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: MÉDICO – ESPECIALIDADE: CLÍNICO-GERAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: CIRURGIÃO-DENTISTA – ESPECIALIDADE: ODONTOPEDIATRA' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: PSICÓLOGO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA – ESPECIALIDADE: NUTRICIONISTA' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB A' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: CUIDADOR' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB D' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – MATEMÁTICA' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – LÍNGUA PORTUGUESA' amb | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – INGLÊS' ambíguas entre | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – HISTÓRIA' ambíguas ent | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – GEOGRAFIA' ambíguas en | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – CIÊNCIAS' ambíguas ent | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB C – ARTE' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N AO N / CARGO N: PROFESSOR DE EDUCAÇÃO BÁSICA – PEB B' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: AGENTE DE SUPORTE AO NEGÓCIO – ESPECIALIDADE: ASSISTENTE A | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: TÉCNICO DE SISTEMAS DE SANEAMENTO – ESPECIALIDADE: TÉCNICO | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: ANALISTA DE SUPORTE AO NEGÓCIO – ESPECIALIDADE: CONTADOR'  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: ANALISTA DE SUPORTE AO NEGÓCIO – ESPECIALIDADE: ANALISTA D | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: ANALISTA DE SUPORTE AO NEGÓCIO – ESPECIALIDADE: ADMINISTRA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: ANALISTA DE SISTEMAS DE SANEAMENTO – ESPECIALIDADE: GEÓGRA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N E N / CARGO N: ANALISTA DE SISTEMAS DE SANEAMENTO – ESPECIALIDADE: ENGENH | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: ANALISTA AMBIENTAL – ESPECIALIDADE: ENGENHARIA QUÍMICA' ambígu | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA OS CARGOS N A N / CARGO N: TÉCNICO UNIVERSITÁRIO DE DESENVOLVIMENTO – FUNÇÃO: JORNALISTA' | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA O CARGO DE TÉCNICO / CARGO N: ANALISTA MINISTERIAL – ESPECIALIDADE: CIÊNCIAS CONTÁBEIS' a | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS GERAIS PARA O CARGO N' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS – ESPECIALIDADE N: TECNOLOGIA DA INFORMAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS ‐ PROGRAMA MULTIPROFISSIONAL EM ATENÇÃO BÁSICA ‐ ÁREA PROFISSIONAL: ODONTOLOGIA E PROGRAM | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA LEGISLATIVO – ÁREA: CONTROLE INTERNO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N: ESPECIALISTA FEDERAL EM ASSISTÊNCIA À EXECUÇÃO PENAL - ÁREA: SERVIÇO SOCIAL' a | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA LEGISLATIVO – ÁREA: CONSULTORIA TÉCNICA LEGISLATIVA' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N: ESPECIALISTA FEDERAL EM ASSISTÊNCIA À EXECUÇÃO PENAL - ÁREA: MÉDICO PSIQUIATRA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA LEGISLATIVO – ÁREA: ARQUITETURA E URBANISMO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS / CARGO N: ANALISTA LEGISLATIVO – ÁREA: ENGENHARIA ELÉTRICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS - PROGRAMA MULTIPROFISSIONAL EM ATENÇÃO BÁSICA - ÁREA PROFISSIONAL: SAÚDE COLETIVA' sem p | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECÍFICOS - PROGRAMA MULTIPROFISSIONAL EM ATENÇÃO BÁSICA - ÁREA PROFISSIONAL: ENFERMAGEM' sem prova | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS ESPECIFÍCOS GRUPO II - DISCIPLINA: BIOLOGIA / GRUPO II - DISCIPLINA: LÍNGUA PORTUGUESA' ambíguas entr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS COMPLEMENTARES PARA OS CARGOS N, N E N / CARGO N: ANALISTA DE PLANEJAMENTO, GESTÃO E INFRAESTRUTURA E | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS COMPLEMENTARES PARA OS CARGOS N, N E N / CARGO N: PESQUISADOR EM PROPRIEDADE INDUSTRIAL – ÁREA DE CON | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS – BLOCO II – PARA OS CARGOS N, N E N / CARGO N: PERITO CRIMINAL FEDERAL – ÁREA N: INFORMÁTICA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS SOMENTE PARA O CARGO N / CARGO N: ANALISTA DE TRÂNSITO – ESPECIALIDADE: ESTATÍSTICA' ambíguas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS SOMENTE PARA O CARGO N / CARGO N: ANALISTA DE REGULAÇÃO – ESPECIALIDADE: ENGENHARIA ELÉTRICA' | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS SOMENTE PARA O CARGO N / CARGO N: GESTOR DE APOIO ÀS ATIVIDADES POLICIAIS CIVIS – ESPECIALIDA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ANALISTA EM DESENVOLVIMENTO REGIONAL – ÁREA: ENGENHARIA MECÂN | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM REGULAÇÃO DE SERVIÇOS PÚBLICOS DE TELECOMUNIC | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM REGULAÇÃO DE AVIAÇÃO CIVIL – ÁREA N' ambíguas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM GESTÃO DE TELECOMUNICAÇÕES – ANALISTA DE TECN | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: AUDITOR FISCAL CONTÁBIL-FINANCEIRO DA RECEITA ESTADUAL' ambíg | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: TECNOLOGISTA PLENO N – N – ÁREA DE ATUAÇÃO: DESERTIFICAÇÃO (C | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: PROFESSOR – ESPECIALIDADE: INGLÊS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: PROFESSOR – ESPECIALIDADE: HISTÓRIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM GESTÃO DE TELECOMUNICAÇÕES – ENGENHEIRO – SUB | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA TODOS OS CARGOS / CARGO N: ESPECIALISTA EM GESTÃO DE TELECOMUNICAÇÕES – CONTADOR' ambígu | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS PERFIS N E N / PERFIL N: AQUISIÇÕES E JURÍDICO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS EMPREGOS N E N / EMPREGO N: ANALISTA DE GEOTECNOLOGIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS EMPREGOS N E N / EMPREGO N: ASSISTENTE DE TECNOLOGIA DA INFORMAÇÃO' ambíguas entre N  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS EMPREGOS N E N A N' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL SUPERIOR (EXCETO CARGO N: PROCURADOR LEGISLATIVO) / CARGO N: APOIO AD | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL MÉDIO / ÊNFASE N: PROJETOS, CONSTRUÇÃO E MONTAGEM – MECÂNICA' ambígua | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL MÉDIO / CARGO N: ANALISTA JÚNIOR – ÊNFASE: JURÍDICO' ambíguas entre N | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL MÉDIO / CARGO N: ENGENHEIRO JÚNIOR – ÊNFASE: PROJETOS E OBRAS, CIVIL' | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL FUNDAMENTAL / CARGO N: AUXILIAR ADMINISTRATIVO' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL FUNDAMENTAL / CARGO N: ENGENHEIRO AMBIENTAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL UNIVERSITÁRIO JUNIOR – FUNÇÃO: BIÓLO | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL UNIVERSITÁRIO JUNIOR – FUNÇÃO: ADVOG | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL TÉCNICO I – FUNÇÃO: TÉCNICO EM MECÂN | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL TÉCNICO I – FUNÇÃO: TÉCNICO EM ELETR | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL UNIVERSITÁRIO JUNIOR – FUNÇÃO: REPÓR | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL UNIVERSITÁRIO JUNIOR – FUNÇÃO: RELAÇ | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS DE N A N / CARGO N: PROFISSIONAL DE NÍVEL UNIVERSITÁRIO JUNIOR – FUNÇÃO: ENGEN | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: TÉCNICO JUDICIÁRIO ‐ ÁREA DE ATIVIDADE: ADMINISTRATIVA' ambíg | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: ANALISTA JUDICIÁRIO ‐ ÁREA DE ATIVIDADE: JUDICIÁRIA ‐ ESPECIA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: TÉCNICO JUDICIÁRIO ‐ ÁREA DE ATIVIDADE: APOIO ESPECIALIZADO ‐ | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N AO N / CARGO N: ANALISTA DE PROCURADORIA – ESPECIALIDADE: DIREITO' ambíguas  | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: PERITO CRIMINAL – ESPECIALIDADE: ENGENHARIA CIVIL' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: PERITO CRIMINAL – ESPECIALIDADE: FÍSICA' ambíguas entre N pro | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N, N, N, N E N / CARGO N: AUDITOR DE CONTROLE EXTERNO – ÁREA: CONTABILIDADE' a | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N, N, N, N E N / CARGO N: AUDITOR DE CONTROLE EXTERNO – ÁREA: ADMINISTRAÇÃO' a | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: JUDICIÁRIA – ESPECIALIDADE: OFICI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: JUDICIÁRIA' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: ANALISTA DO CNMP – ÁREA: TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇ | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N E N / CARGO N: ANALISTA DO CNMP – ÁREA: APOIO TÉCNICO ESPECIALIZADO – ESPECI | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N AO N / CARGO N: MÉDICO PSIQUIATRA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N AO N / CARGO N: CONTADOR' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N AO N / CARGO N: ANALISTA REGULADOR – PERFIL: DIREITO' ambíguas entre N prova | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N A N / CARGO N: TÉCNICO DE NÍVEL SUPERIOR – ESPECIALIDADE: ADMINISTRATIVO' am | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N A N / CARGO N: ANALISTA AMBIENTAL – ESPECIALIDADE: CONTABILIDADE' ambíguas e | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N A N / CARGO N: ANALISTA AMBIENTAL – ESPECIALIDADE: COMUNICAÇÃO SOCIAL' ambíg | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA OS CARGOS N A N / CARGO N: ASSISTENTE AMBIENTAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO DE SOLDADO DE PRAÇA POLICIAL / CARGO N: TENENTE PM – MÉDICO-VETERINÁRIO' ambígua | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO DE SOLDADO DE PRAÇA POLICIAL / CARGO N: TENENTE PM – MÉDICO' ambíguas entre N pr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: ANALISTA ADMINISTRATIVO DE PROCURADORIA – ESPECIALIDADE: RECURSOS H | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: ASSISTENTE EM ADMINISTRAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: ENGENHEIRO AGRONÔMICO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: TÉCNICO DE TECNOLOGIA DA INFORMAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N / CARGO N: ENGENHEIRO AGRÔNOMO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N E PARA OS CARGOS DE N A N' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICOS PARA O CARGO N E PARA OS CARGOS DE N A N / CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIA | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICO PARA TODOS AS ÊNFASES / ÊNFASE N: SUPRIMENTO DE BENS E SERVIÇOS – ADMINISTRAÇÃO' ambíguas entr | 1 |
| gabarito | justificativas da seção 'CONHECIMENTOS BÁSICO PARA TODOS AS ÊNFASES / ÊNFASE N: PROJETOS, CONSTRUÇÃO E MONTAGEM – MECÂNICA' ambíguas entre N | 1 |
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
| gabarito | justificativas da seção 'CARGO DE ASSISTENTE I.N – ÁREA DE CONCENTRAÇÃO: APOIO ADMINISTRATIVO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: PROFESSOR DA EDUCAÇÃO BÁSICA – DISCIPLINA: INFORMÁTICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ESPECIALISTA PORTUÁRIO – ÁREA: ARQUITETURA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: OFICIAL DE JUSTIÇA AVALIADOR' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: CIÊNCIAS CONTÁBEIS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – CONTABILIDADE' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: PROFESSOR – DO Nº AO Nº ANO – ENSINO FUNDAMENTAL – ESPECIALIDADE: CIÊNCIAS' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – COMUNICAÇÃO SOCIAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE PREVIDÊNCIA COMPLEMENTAR – ÁREA N: JURÍDICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA ADMINISTRATIVO – ÁREA: DIREITO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: DIREITO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – BIBLIOTECONOMIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE PREVIDÊNCIA COMPLEMENTAR – ÁREA N: GESTÃO DE INVESTIMENTOS E RISCOS DE INVESTIMENTOS' ambíguas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE CONTROLE EXTERNO – ÁREA DE GRADUAÇÃO/ESPECIALIDADE: CIÊNCIAS ECONÔMICAS' ambíguas entre N prov | 1 |
| gabarito | justificativas da seção 'CARGO N: TÉCNICO MINISTERIAL – ESPECIALIDADE: AUXILIAR ADMINISTRATIVO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA PORTUÁRIO II – ÁREA: CONTRATOS' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – ARQUIVOLOGIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE CONTROLE EXTERNO – ÁREA DE GRADUAÇÃO/ESPECIALIDADE: CIÊNCIA DA COMPUTAÇÃO' ambíguas entre N pr | 1 |
| gabarito | justificativas da seção 'CARGO N: DELEGADO DE POLÍCIA CIVIL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ÁREA: APOIO ESPECIALIZADO – ESPECIALIDADE: ANÁLISE DE SISTEMAS' sem prova correspond | 1 |
| gabarito | justificativas da seção 'CARGO N: SOLDADO COMBATENTE' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: DATILOSCOPISTA POLICIAL' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE: ADMINISTRAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE PREVIDÊNCIA COMPLEMENTAR – ÁREA N: GOVERNANÇA, AUDITORIA, CONTROLE E CONFORMIDADE' ambíguas en | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE CONTROLE EXTERNO – ÁREA DE GRADUAÇÃO/ESPECIALIDADE: CIÊNCIAS ATUARIAIS' ambíguas entre N prova | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – TAQUIGRAFIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: TÉCNICO BANCÁRIO III – ÁREA: INFORMÁTICA – ESPECIALIDADE: DESENVOLVIMENTO' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: OFICIAL COMBATENTE' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CARGO N: AUXILIAR DE LEGISTA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ÁREA: ADMINISTRATIVA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA ADMINISTRATIVO DE CONTROLE EXTERNO – ÁREA DE GESTÃO – ESPECIALIDADE SERVIÇOS TÉCNICOS E ADMINISTR | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – PSICOLOGIA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: FISCAL DE ARRECADAÇÃO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – MEDICINA DO TRABALHO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: ESTATÍSTICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA DE GESTÃO DE RESÍDUOS SÓLIDOS – ESPECIALIDADE: ENGENHARIA QUÍMICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – ESPECIALIDADE: ENGENHARIA MECÂNICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – ENGENHARIA ELÉTRICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: PERITO CRIMINAL – ÁREA N: CIÊNCIA DA COMPUTAÇÃO, ENGENHARIA DA COMPUTAÇÃO OU SISTEMAS DE INFORMAÇÃO' ambíg | 1 |
| gabarito | justificativas da seção 'CARGO N: GESTOR EM PLANEJAMENTO DE EDUCAÇÃO – ÁREA: PLANEJAMENTO' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ESPECIALISTA PORTUÁRIO – ÁREA: ENGENHARIA MECÂNICA' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CARGO N: ANALISTA JUDICIÁRIO – APOIO ESPECIALIZADO – ESPECIALIDADE – ENFERMAGEM' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'CN - CONHECIMENTOS COMPLEMENTARES PARA AS OPÇÕES N, N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'CN - CONHECIMENTOS COMPLEMENTARES PARA A OPÇÃO N' sem prova correspondente | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – ENFERMEIRO DO TRABALHO – UGP' ambí | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO II – UGP' ambíguas entre N provas | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE INTERFEDERATIVO – ESPECIALISTA EM GESTÃO INTERF | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – UINFRA (FISCALIZAÇÃO DE OBRAS) – E | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – UINFRA (ENGENHARIA E ARQUITETURA)  | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – PERFIL N – USI' ambíguas entre N p | 1 |
| gabarito | justificativas da seção 'BLOCO II / PROVA DE CONHECIMENTOS ESPECÍFICOS / CARGO N: ASSISTENTE DE PROJETO – PERFIL N – UDIGIS' ambíguas entre  | 1 |
| gabarito | justificativas da seção 'BLOCO I - CBN / PROVA DE CONHECIMENTOS BÁSICOS PARA OS CARGOS DE NÍVEL MÉDIO' sem prova correspondente | 1 |
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
| validacao | prova sem gabarito vinculado | 123 |
| validacao | N questão(ões) sem gabarito: […] | 51 |
| validacao | nº de itens extraídos (N) difere do gabarito (N) | 44 |

## Observações de método

- Nada é estimado: resposta, ano ou texto que não pôde ser lido fica NULL e gera pendência.
- `alterada=1` só quando há evidência (preliminar e definitivo publicados, ou tabela de justificativas). O site costuma retirar o gabarito preliminar após o definitivo, então a ausência de alteração não é prova de que o item não mudou.
- Itens de opção de língua estrangeira (ex.: itens 1–10 em espanhol e em inglês) são guardados por língua (`questao.variante`, `gabarito_bruto.variante`): na prova pelo título 'LÍNGUA X' de cada bloco e no gabarito pela cor da célula e a legenda. Conflitos que a legenda não resolve ficam sem resposta.
- Versões de acessibilidade (adaptada, superampliada, ledor, braile, VLibras) foram ignoradas.
- Números de itens ofuscados (substituição de glifos, comum em 2015–2017) são decodificados pela restrição de sequência consecutiva.


### Concursos sem detalhe na API

`ANATEL_14`, `ANTAQ_14`, `DEPEN_15`, `DPE_PE_14_DEFENSOR`, `DPE_RN_15_DEFENSOR`, `DPF_14_AGENTE`, `DPU_15_ADMINISTRATIVO`, `FUB_15_1`, `FUNPRESP_15`, `MEC_15_TEMPORARIO`, `MPU_15`, `MP_15_ENAP`, `PREF_SALVADOR_15_PROCURADOR`, `SEC_BA_15_DIRETOR_E_VICE`, `SES_DF_15_MULTIPROFISSIONAL`, `SES_DF_15_MULTIPROFISSIONAL_2`, `SES_DF_15_RESIDENCIA`, `SES_DF_16_MULTIPROFISSIONAL`, `SES_DF_16_RESIDENCIA`, `STJ_15`, `TCE_PR_15_AUDITOR`, `TCE_RN_15_SERVIDOR`, `TCE_SC_15`, `TC_RN_15_AUDITOR`, `TELEBRAS_15`, `TESTE_2029`, `TJDFT_15_JUIZ`, `TJDFT_15_JUIZ_2`, `TJ_AM_15_JUIZ`, `TJ_PB_15_JUIZ`, `TRE_MT_15`, `TRE_PE_15`, `TRE_PI_15`, `TRE_RS_15`, `TRF1_15_JUIZ`
