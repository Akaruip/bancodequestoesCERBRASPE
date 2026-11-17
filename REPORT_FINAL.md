# Relatório final — banco de questões Cebraspe

Gerado em 2026-11-17T11:42:43+00:00 a partir de `cebraspe.db`.

## Visão geral

| Métrica | Valor |
|---|---|
| Concursos listados | 500 |
| Concursos com detalhe na API | 465 |
| Concursos com provas extraídas | 426 |
| Documentos baixados | 11596 (3.08 GB) |
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


Questões objetivas com **texto de apoio** (`texto_id`): **36822**, das quais 2000 ligadas pelo rótulo citado no comando ("do texto CB1A1").


Provas com **somente o gabarito preliminar** (definitivo não publicado ou não vinculado): **131** (9039 questões). Nelas `resposta_definitiva` fica vazia e a resposta está em `resposta_preliminar`; cada prova tem a pendência de validação correspondente.

| Com definitivo | Com preliminar | Anuladas | Alteradas | Com justificativa | Com padrão de resposta |
|---|---|---|---|---|---|
| 200973 | 26163 | 6127 | 1676 | 14446 | 6129 |

## Disciplinas (Fase 5)

Questões com **disciplina** identificada: **132562** (60.4% de 219526); com **assunto** literal do comando: **155210** (70.7%). As provas do Cebraspe quase nunca têm título de disciplina: a disciplina vem do idioma da opção de língua (`variante`), do título do bloco quando ele é uma disciplina (`titulo_pdf`), do idioma do comando (`regra_comando`), do conteúdo programático do edital de abertura comparado ao assunto literal (`edital_assunto`), da tabela de palavras-chave aplicada ao assunto (`regra_assunto`), da única disciplina/área do cargo no edital (`edital_unica`) ou da área declarada na prova quando o concurso não tem conteúdo programático (`area_prova`). Sem nenhuma dessas fontes fica NULL.


Editais de abertura lidos com conteúdo programático: **384** concursos; sem conteúdo programático legível: **35** (pendência `disciplina`).

| disciplina_fonte | Questões |
|---|---|
| (não identificada) | 86964 |
| edital_assunto | 62273 |
| regra_assunto | 34409 |
| edital_unica | 32125 |
| area_prova | 1458 |
| regra_comando | 1449 |
| titulo_pdf | 748 |
| variante | 100 |

| Disciplina | Questões | CE | ME | DISC |
|---|---|---|---|---|
| Língua Portuguesa | 8529 | 6914 | 1155 | 460 |
| Tecnologia da Informação | 8305 | 7683 | 557 | 65 |
| Direito Administrativo | 7135 | 5594 | 1406 | 135 |
| Direito Constitucional | 4534 | 3464 | 1041 | 29 |
| Direito Financeiro e Orçamento Público | 3908 | 3247 | 446 | 215 |
| Administração Geral | 3898 | 3545 | 241 | 112 |
| Administração Pública | 3032 | 2586 | 390 | 56 |
| Contabilidade | 2626 | 2122 | 418 | 86 |
| Educação e Pedagogia | 2539 | 2155 | 359 | 25 |
| Psicologia | 2493 | 2101 | 292 | 100 |
| Enfermagem | 2276 | 1975 | 301 | 0 |
| Noções de Informática | 2259 | 1937 | 217 | 105 |
| Língua Inglesa | 2066 | 1702 | 226 | 138 |
| Serviço Social | 2042 | 1662 | 245 | 135 |
| Direito Tributário | 1867 | 1252 | 597 | 18 |
| Auditoria | 1682 | 1318 | 359 | 5 |
| Arquivologia | 1601 | 1437 | 164 | 0 |
| Economia | 1554 | 1229 | 196 | 129 |
| Direito Penal | 1530 | 1044 | 470 | 16 |
| Contabilidade Pública | 1482 | 1284 | 176 | 22 |
| Direito Previdenciário | 1480 | 1316 | 155 | 9 |
| Saúde Pública e SUS | 1473 | 1338 | 135 | 0 |
| Engenharia Civil | 1419 | 1270 | 138 | 11 |
| Direito Civil | 1386 | 961 | 405 | 20 |
| Direito Processual Penal | 1307 | 860 | 433 | 14 |
| Estatística | 1302 | 1148 | 154 | 0 |
| Direito Processual Civil | 1274 | 853 | 413 | 8 |
| Biblioteconomia | 1252 | 1104 | 73 | 75 |
| Engenharia Elétrica | 1156 | 903 | 117 | 136 |
| Gestão de Pessoas | 1094 | 1004 | 60 | 30 |
| Raciocínio Lógico e Matemática | 996 | 793 | 201 | 2 |
| Ética no Serviço Público | 984 | 822 | 42 | 120 |
| Legislação Específica | 965 | 804 | 160 | 1 |
| Legislação | 865 | 759 | 106 | 0 |
| Arquitetura e Urbanismo | 815 | 784 | 31 | 0 |
| Controle Externo | 755 | 596 | 159 | 0 |
| Farmácia | 748 | 665 | 83 | 0 |
| Odontologia | 722 | 535 | 187 | 0 |
| Jornalismo | 691 | 645 | 46 | 0 |
| Engenharia Mecânica | 690 | 577 | 46 | 67 |
| Medicina do Trabalho | 688 | 529 | 159 | 0 |
| Bloco Ii | 634 | 634 | 0 | 0 |
| Direito Ambiental | 620 | 457 | 157 | 6 |
| Geografia | 620 | 462 | 158 | 0 |
| Biologia | 546 | 459 | 87 | 0 |
| Direito Empresarial | 546 | 381 | 165 | 0 |
| Fisioterapia | 540 | 525 | 15 | 0 |
| Direitos Humanos | 486 | 404 | 82 | 0 |
| Direito do Trabalho | 476 | 341 | 135 | 0 |
| Medicina | 476 | 403 | 73 | 0 |
| Atualidades e Realidade Regional | 471 | 230 | 241 | 0 |
| Comunicação Social | 448 | 418 | 30 | 0 |
| Noções de Administração | 440 | 399 | 18 | 23 |
| Nutrição | 436 | 397 | 39 | 0 |
| Química | 416 | 273 | 143 | 0 |
| Educação Física | 397 | 321 | 76 | 0 |
| Terapia Ocupacional | 394 | 377 | 17 | 0 |
| Engenharia Ambiental | 382 | 286 | 46 | 50 |
| Língua Espanhola | 374 | 209 | 40 | 125 |
| Matemática | 371 | 300 | 65 | 6 |
| História | 367 | 276 | 91 | 0 |
| Física | 364 | 260 | 104 | 0 |
| Fonoaudiologia | 363 | 341 | 22 | 0 |
| Psiquiatria | 362 | 274 | 88 | 0 |
| Legislação Educacional | 349 | 347 | 2 | 0 |
| Desenvolvimento de Sistemas | 343 | 322 | 13 | 8 |
| Direito da Criança e do Adolescente | 325 | 241 | 79 | 5 |
| Administração | 318 | 275 | 43 | 0 |
| Cardiologia | 305 | 305 | 0 | 0 |
| Direito Processual do Trabalho | 293 | 211 | 82 | 0 |
| Legislação de Trânsito | 286 | 271 | 15 | 0 |
| Medicina Veterinária | 279 | 170 | 109 | 0 |
| Audiovisual | 274 | 274 | 0 | 0 |
| Arquitetura | 273 | 226 | 47 | 0 |
| Atualidade Brasileira | 273 | 273 | 0 | 0 |
| Geologia | 265 | 188 | 6 | 71 |
| Clínica Geral | 264 | 224 | 40 | 0 |
| Infraestrutura em Ti | 261 | 261 | 0 | 0 |
| Sustentabilidade | 257 | 243 | 14 | 0 |
| Clínica Médica | 255 | 248 | 7 | 0 |
| Segurança do Trabalho | 249 | 164 | 15 | 70 |
| Ciências | 227 | 197 | 30 | 0 |
| Urologia | 226 | 226 | 0 | 0 |
| Arte | 221 | 156 | 65 | 0 |
| Direito do Consumidor | 219 | 149 | 70 | 0 |
| Relações Públicas | 219 | 219 | 0 | 0 |
| Mastologia | 216 | 216 | 0 | 0 |
| Sociologia | 215 | 167 | 48 | 0 |
| Engenharia Química | 214 | 140 | 74 | 0 |
| Telecomunicações | 210 | 170 | 40 | 0 |
| Agronomia | 205 | 178 | 27 | 0 |
| Programação de Sistemas | 203 | 111 | 92 | 0 |
| Engenharia Eletrônica | 183 | 143 | 40 | 0 |
| Análises Clínicas | 180 | 180 | 0 | 0 |
| Filosofia | 180 | 133 | 47 | 0 |
| Obras Hídricas | 172 | 137 | 15 | 20 |
| Ortopedia e Traumatologia | 170 | 170 | 0 | 0 |
| Técnico Educacional | 169 | 128 | 0 | 41 |
| Direito Eleitoral | 163 | 51 | 112 | 0 |
| Biomedicina | 158 | 158 | 0 | 0 |
| Técnico de Segurança do Trabalho | 154 | 154 | 0 | 0 |
| Engenharia de Produção | 153 | 92 | 0 | 61 |
| Comunicação | 147 | 71 | 76 | 0 |
| Pediatria | 147 | 118 | 29 | 0 |
| Noções em Segurança do Trabalho | 145 | 0 | 145 | 0 |
| Técnico Industrial | 140 | 140 | 0 | 0 |
| Análise de Sistemas | 136 | 116 | 20 | 0 |
| Segurança Judiciária | 135 | 96 | 39 | 0 |
| Hematologia e Hemoterapia | 134 | 134 | 0 | 0 |
| Radioterapia | 134 | 134 | 0 | 0 |
| Publicidade e Propaganda | 131 | 131 | 0 | 0 |
| Governança | 128 | 128 | 0 | 0 |
| Geografia Geografia | 126 | 116 | 10 | 0 |
| Medicina Legal | 124 | 72 | 52 | 0 |
| Engenharia de Segurança do Trabalho | 122 | 121 | 1 | 0 |
| Engenharia Florestal | 120 | 67 | 53 | 0 |
| Transplante de Rim - Nefrologia | 120 | 120 | 0 | 0 |
| Engenharia Elétrica/eletrônica | 119 | 119 | 0 | 0 |
| Obras Rodoviárias | 118 | 100 | 14 | 4 |
| Superior | 118 | 0 | 118 | 0 |
| Teoria da Música | 118 | 27 | 91 | 0 |
| Engenharia Agronômica | 117 | 52 | 0 | 65 |
| Engenharia de Agrimensura | 117 | 40 | 39 | 38 |
| Análise de Dados e Informações | 116 | 116 | 0 | 0 |
| Neurologia | 116 | 116 | 0 | 0 |
| Obstetrícia | 116 | 116 | 0 | 0 |
| Legislação Especial | 115 | 96 | 19 | 0 |
| Libras | 115 | 103 | 12 | 0 |
| Artes | 114 | 114 | 0 | 0 |
| Cirurgia Básica/clínica Médica/infectologia/medicina da Família e Comunidade/obstetrícia e Ginecologia/oftalmologia/otorrinolaringologia/patologia/pediatria/psiquiatria/radiologia e Diagnóstico por Imagem/radioterapia/dermatologia | 112 | 112 | 0 | 0 |
| Nefrologia | 112 | 112 | 0 | 0 |
| Obras de Edificações | 111 | 90 | 14 | 7 |
| Coloproctologia | 110 | 110 | 0 | 0 |
| Noções de Direito Público | 110 | 110 | 0 | 0 |
| Otorrinolaringologia | 110 | 110 | 0 | 0 |
| Técnico de Radiologia | 110 | 110 | 0 | 0 |
| Terapia Intensiva Pediátrica | 108 | 108 | 0 | 0 |
| Infraestrutura de Ti | 106 | 99 | 7 | 0 |
| Neonatologia | 106 | 106 | 0 | 0 |
| Reumatologia | 105 | 105 | 0 | 0 |
| Anestesiologia | 103 | 103 | 0 | 0 |
| Iso 9000 | 103 | 0 | 103 | 0 |
| Orçamento | 103 | 103 | 0 | 0 |
| Direito Internacional | 102 | 68 | 16 | 18 |
| Pneumologia | 100 | 100 | 0 | 0 |
| Hepatologia | 99 | 99 | 0 | 0 |
| Infectologia | 99 | 99 | 0 | 0 |
| Engenharia Agronômica/agronomia | 97 | 97 | 0 | 0 |
| Cirurgia Torácica | 96 | 96 | 0 | 0 |
| Matemática Matemática | 96 | 93 | 3 | 0 |
| Cirurgia Plástica | 95 | 95 | 0 | 0 |
| Cirurgia Vascular | 95 | 95 | 0 | 0 |
| Cirurgia de Cabeça e Pescoço | 95 | 95 | 0 | 0 |
| Endoscopia Digestiva | 95 | 95 | 0 | 0 |
| Psiquiatra | 95 | 46 | 49 | 0 |
| Atuária | 94 | 61 | 33 | 0 |
| Radiologia e Diagnóstico por Imagem | 94 | 94 | 0 | 0 |
| Secretariado Executivo | 94 | 94 | 0 | 0 |
| Neurocirurgia | 92 | 92 | 0 | 0 |
| Engenharia de Minas | 91 | 91 | 0 | 0 |
| Cirurgia Pediátrica | 88 | 88 | 0 | 0 |
| Controle Interno | 88 | 76 | 12 | 0 |
| Fiscalização de Contratos de Ti | 88 | 79 | 9 | 0 |
| Hemodinâmica e Cardiologia Intervencionista | 88 | 88 | 0 | 0 |
| Terapia Intensiva | 88 | 88 | 0 | 0 |
| Planejamento | 86 | 86 | 0 | 0 |
| Técnico em Radiologia | 86 | 67 | 19 | 0 |
| Gastroenterologia | 83 | 83 | 0 | 0 |
| Geriatria | 83 | 83 | 0 | 0 |
| Inglês | 83 | 60 | 23 | 0 |
| Terapia Intensiva Neonatal | 82 | 82 | 0 | 0 |
| Desenvolvimento de Sistemas Desenvolvimento de Sistemas | 78 | 78 | 0 | 0 |
| Educação Física Educação Física | 76 | 68 | 8 | 0 |
| Transportes Aquaviários | 76 | 76 | 0 | 0 |
| Odontopediatria Odontopediatria | 75 | 75 | 0 | 0 |
| Noções de Legislação e Normas Ambientais | 74 | 0 | 74 | 0 |
| Legislação e Normas Ambientais | 73 | 14 | 59 | 0 |
| Sociologia Sociologia | 73 | 60 | 13 | 0 |
| Análise de Sistema (suporte e Infraestrutura) | 72 | 72 | 0 | 0 |
| Hidrologia | 72 | 32 | 40 | 0 |
| Tecnologia | 72 | 72 | 0 | 0 |
| Técnico em Saúde Bucal | 72 | 0 | 72 | 0 |
| Meio Ambiente | 71 | 71 | 0 | 0 |
| Biologia Biologia | 70 | 62 | 8 | 0 |
| Cardiopediatria | 70 | 70 | 0 | 0 |
| Cartografia | 70 | 0 | 0 | 70 |
| Cirurgia Cardíaca | 70 | 70 | 0 | 0 |
| Cirurgia-geral | 70 | 70 | 0 | 0 |
| Dermatologia | 70 | 70 | 0 | 0 |
| Direito Notarial e Registral | 70 | 4 | 66 | 0 |
| Endocrinologia | 70 | 70 | 0 | 0 |
| Engenharia Cartográfica | 70 | 70 | 0 | 0 |
| Engenharia Elétrica, Engenharia Eletrônica, Engenharia de Redes de Comunicação Ou Engenharia de Telecomunicações | 70 | 0 | 70 | 0 |
| Engenharia Mecânica Ou Engenharia Mecatrônica | 70 | 0 | 70 | 0 |
| Filosofia Filosofia | 70 | 63 | 7 | 0 |
| Física Forense | 70 | 70 | 0 | 0 |
| Geologia Forense | 70 | 70 | 0 | 0 |
| Ginecologia | 70 | 70 | 0 | 0 |
| Intensivista | 70 | 70 | 0 | 0 |
| Laboratório | 70 | 70 | 0 | 0 |
| Manejo, Conservação e Reabilitação da Fauna Silvestre | 70 | 70 | 0 | 0 |
| Mecânica | 70 | 0 | 70 | 0 |
| Medicina (cardiologia) | 70 | 70 | 0 | 0 |
| Mineração | 70 | 70 | 0 | 0 |
| Neuropediatria | 70 | 70 | 0 | 0 |
| Noções de Produção Editorial | 70 | 0 | 0 | 70 |
| Nutrição Clínica | 70 | 0 | 0 | 70 |
| Oftamologia | 70 | 70 | 0 | 0 |
| Ortopedia | 70 | 70 | 0 | 0 |
| Química, Química Industrial Ou Engenharia Química | 70 | 0 | 70 | 0 |
| Refrigeração | 70 | 70 | 0 | 0 |
| Técnico Desportivo | 70 | 0 | 0 | 70 |
| Técnico de Laboratório | 70 | 70 | 0 | 0 |
| Ótica | 70 | 70 | 0 | 0 |
| Ciências Biológicas e Biomedicina | 69 | 0 | 69 | 0 |
| Artes Arte | 68 | 68 | 0 | 0 |
| Diagnóstico por Imagem | 68 | 68 | 0 | 0 |
| Engenharia Agronômica, Geologia, Engenharia Ambiental Ou Engenharia Florestal | 68 | 0 | 68 | 0 |
| Engenharia de Telecomunicações | 68 | 68 | 0 | 0 |
| Legislação, Compreensão da Libras e Ética Profissional | 68 | 68 | 0 | 0 |
| Eletricista Ou Eletrônico Engenharia Elétrica/eletrônica | 67 | 67 | 0 | 0 |
| Ensino Religioso | 67 | 67 | 0 | 0 |
| Necropsia | 67 | 67 | 0 | 0 |
| Odontologia (bucomaxilo) | 67 | 67 | 0 | 0 |
| Radiologia | 67 | 67 | 0 | 0 |
| Web Design | 67 | 67 | 0 | 0 |
| Ciência e Tecnologia | 66 | 63 | 3 | 0 |
| Eletricidade e Comunicação | 66 | 66 | 0 | 0 |
| História História | 66 | 60 | 6 | 0 |
| Telecomunicações Engenharia de Telecomunicações | 66 | 66 | 0 | 0 |
| Direito Econômico | 65 | 52 | 8 | 5 |
| Produção Cultural | 65 | 65 | 0 | 0 |
| Administrador de Edifícios | 64 | 64 | 0 | 0 |
| Civil Engenharia Civil | 64 | 64 | 0 | 0 |
| Comunicação e Marketing | 64 | 64 | 0 | 0 |
| Odontologia (hospitalar) | 64 | 64 | 0 | 0 |
| Noções de Recursos Materiais | 63 | 63 | 0 | 0 |
| Noções de Gestão Educacional | 62 | 62 | 0 | 0 |
| Governança e Gestão de Ti | 61 | 53 | 0 | 8 |
| Antropologia Forense | 60 | 60 | 0 | 0 |
| Cirurgia e Traumatologia Buco | 60 | 60 | 0 | 0 |
| Fisioterapia Cardiovascular | 60 | 60 | 0 | 0 |
| Fisioterapia Respiratória | 60 | 60 | 0 | 0 |
| Museólogo | 60 | 60 | 0 | 0 |
| Nbr Isso/iec 20000-1 | 60 | 60 | 0 | 0 |
| Organização Judiciária do Distrito Federal e Territórios | 60 | 60 | 0 | 0 |
| Finanças | 59 | 55 | 4 | 0 |
| Nbr Iso 14.001 | 59 | 59 | 0 | 0 |
| Neurofuncional | 59 | 59 | 0 | 0 |
| Taxidermia | 58 | 58 | 0 | 0 |
| Centro Cirúrgico | 57 | 57 | 0 | 0 |
| Engenheiro Civil | 57 | 57 | 0 | 0 |
| Neuropsicologia | 57 | 57 | 0 | 0 |
| Suporte e Infraestrutura | 57 | 50 | 1 | 6 |
| Engenheiro Clínico | 56 | 56 | 0 | 0 |
| Transplantes | 56 | 56 | 0 | 0 |
| Criminologia | 55 | 40 | 15 | 0 |
| Infecção Hospitalar | 55 | 55 | 0 | 0 |
| Análise de Dados | 54 | 45 | 9 | 0 |
| Engenharia de Redes | 53 | 53 | 0 | 0 |
| Didáticos | 52 | 0 | 52 | 0 |
| Jornalista Jornalismo | 52 | 52 | 0 | 0 |
| Urgência e Emergência | 52 | 52 | 0 | 0 |
| Ciências Humanas | 51 | 47 | 4 | 0 |
| Eletrônica | 51 | 31 | 20 | 0 |
| Genética Forense | 51 | 51 | 0 | 0 |
| Noções de Biossegurança | 51 | 0 | 51 | 0 |
| Noções de Serviços de Ti | 51 | 50 | 1 | 0 |
| Radiodiagnóstico | 51 | 51 | 0 | 0 |
| Acre | 50 | 50 | 0 | 0 |
| Anestesiologista | 50 | 30 | 20 | 0 |
| Dermatologista | 50 | 0 | 50 | 0 |
| Gestão e Risco de Investimentos Gestão e Riscos de Investimentos | 50 | 50 | 0 | 0 |
| Neurologista | 50 | 0 | 50 | 0 |
| Noções de Medicina Legal | 50 | 41 | 9 | 0 |
| Ortopedista | 50 | 0 | 50 | 0 |
| Perfusionista | 50 | 50 | 0 | 0 |
| Sistemas de Computação | 50 | 50 | 0 | 0 |
| Urologista | 50 | 0 | 50 | 0 |
| Contratações de Ti | 49 | 49 | 0 | 0 |
| Fiscalização, Gerenciamento e Gestão de Obras e Serviços | 49 | 48 | 1 | 0 |
| Governança, Estratégia e Gestão | 48 | 48 | 0 | 0 |
| Redes Engenharia de Redes | 48 | 48 | 0 | 0 |
| Gestão Hospitalar | 47 | 47 | 0 | 0 |
| Infraestrutura | 47 | 29 | 18 | 0 |
| Noções de Geoprocessamento | 47 | 0 | 47 | 0 |
| Patologia | 47 | 47 | 0 | 0 |
| Pediatra | 47 | 27 | 20 | 0 |
| Revisor de Braille | 47 | 47 | 0 | 0 |
| Medicina Psiquiátrica | 46 | 0 | 16 | 30 |
| Química Química | 46 | 42 | 4 | 0 |
| Segurança Orgânica | 46 | 46 | 0 | 0 |
| Braille | 45 | 45 | 0 | 0 |
| Ciências da Religião | 45 | 27 | 18 | 0 |
| Direito Urbanístico | 45 | 33 | 12 | 0 |
| Saneamento | 45 | 5 | 40 | 0 |
| Equipamento Médico-odontológico | 44 | 44 | 0 | 0 |
| Obras – Planejamento, Normas, Fiscalização e Legislação | 44 | 30 | 14 | 0 |
| Geologia e Mineração | 43 | 43 | 0 | 0 |
| Ciência Política | 42 | 42 | 0 | 0 |
| Engenharia Sanitária | 42 | 7 | 35 | 0 |
| Segurança de Dignitários | 42 | 42 | 0 | 0 |
| Desenvolvimento de Sistemas de Computação | 41 | 33 | 8 | 0 |
| Angiologia | 40 | 40 | 0 | 0 |
| Clínico‐geral | 40 | 0 | 40 | 0 |
| Dentística) Odontologia | 40 | 40 | 0 | 0 |
| Dor | 40 | 40 | 0 | 0 |
| Educação Fiscal | 40 | 40 | 0 | 0 |
| Eletricidade e Telecomunicações | 40 | 0 | 40 | 0 |
| Fotografia | 40 | 40 | 0 | 0 |
| Legislação Ambiental | 40 | 40 | 0 | 0 |
| Mamografia | 40 | 40 | 0 | 0 |
| Medicina Fetal | 40 | 40 | 0 | 0 |
| Normas Institucionais | 40 | 30 | 10 | 0 |
| Noções de Fiscalização | 40 | 8 | 0 | 32 |
| Pneumologia Pediátrica | 40 | 40 | 0 | 0 |
| Radiologia Intervencionista e Angiorradiologia | 40 | 40 | 0 | 0 |
| Reumatologia Pediátrica | 40 | 40 | 0 | 0 |
| Topografia | 40 | 40 | 0 | 0 |
| Ultrassonografia em Ginecologia e Obstetrícia | 40 | 40 | 0 | 0 |
| História da Música | 39 | 39 | 0 | 0 |
| Iii | 39 | 39 | 0 | 0 |
| Legislação Relacionada | 39 | 39 | 0 | 0 |
| Saúde Indígena | 39 | 39 | 0 | 0 |
| Abnt Nbr Iso 22301 | 38 | 38 | 0 | 0 |
| Noções de Administração e Gestão Fiscal | 38 | 38 | 0 | 0 |
| Aquicultura | 37 | 13 | 4 | 20 |
| Comunicação Social – Jornalismo Comunicação | 37 | 37 | 0 | 0 |
| Direito das Pessoas com Deficiência | 37 | 36 | 1 | 0 |
| Econometria | 37 | 37 | 0 | 0 |
| Organizacional | 37 | 37 | 0 | 0 |
| Administração Hospitalar | 36 | 36 | 0 | 0 |
| Atendimento ao Público | 36 | 36 | 0 | 0 |
| Geoprocessamento | 36 | 0 | 36 | 0 |
| História do Maranhão | 36 | 31 | 5 | 0 |
| Arqueologia | 35 | 35 | 0 | 0 |
| Atividade de Inteligência e Legislação Correlata | 35 | 35 | 0 | 0 |
| Cirurgia do Aparelho Digestivo | 35 | 35 | 0 | 0 |
| Direito Processual de Contas | 35 | 18 | 17 | 0 |
| Fundamentos da Educação | 35 | 35 | 0 | 0 |
| Rede de Computadores | 35 | 35 | 0 | 0 |
| Referências Bibliográficas | 35 | 0 | 35 | 0 |
| Regulação e Agências Reguladoras | 35 | 35 | 0 | 0 |
| Tecnologias Digitais e Computação | 35 | 0 | 35 | 0 |
| História do Brasil | 34 | 34 | 0 | 0 |
| Legislação Pertinente ao Cbmal | 34 | 34 | 0 | 0 |
| Medicina Intensiva | 34 | 34 | 0 | 0 |
| Noções de Telecomunicações | 34 | 34 | 0 | 0 |
| Processo Regulatório | 34 | 34 | 0 | 0 |
| Tecnologia e Informação | 34 | 34 | 0 | 0 |
| Infraestrutura e Cibersegurança | 33 | 33 | 0 | 0 |
| Medicina Física e Reabilitação | 33 | 33 | 0 | 0 |
| Médica | 33 | 0 | 33 | 0 |
| Resoluções Cau/br | 33 | 33 | 0 | 0 |
| Gestão e Riscos de Investimentos | 32 | 32 | 0 | 0 |
| Infectologia Pediátrica | 32 | 32 | 0 | 0 |
| Analista Técnico Ii – Comércio Exterior Comércio Exterior | 31 | 0 | 31 | 0 |
| Infraestrutura Rodoviária | 31 | 31 | 0 | 0 |
| Ocupacional | 31 | 31 | 0 | 0 |
| Organização da Justiça Militar da União | 31 | 31 | 0 | 0 |
| Saúde do Adulto | 31 | 31 | 0 | 0 |
| Acupunturista | 30 | 0 | 30 | 0 |
| Angiologista | 30 | 0 | 30 | 0 |
| Cardiologista | 30 | 0 | 30 | 0 |
| Contratações de Tic | 30 | 30 | 0 | 0 |
| De Projetos e Programas em Ct&i | 30 | 30 | 0 | 0 |
| Elétrica | 30 | 0 | 30 | 0 |
| Endocrinologista | 30 | 0 | 30 | 0 |
| Gastroenterologista | 30 | 0 | 30 | 0 |
| Gastroenterologista Infantil | 30 | 0 | 30 | 0 |
| Genética Médica | 30 | 30 | 0 | 0 |
| Gestão de Ti | 30 | 25 | 5 | 0 |
| Ginecologista | 30 | 0 | 30 | 0 |
| Hematologista | 30 | 0 | 30 | 0 |
| Infectologista | 30 | 0 | 30 | 0 |
| Inovação | 30 | 30 | 0 | 0 |
| Legislação e Ética na Adminstração Pública | 30 | 30 | 0 | 0 |
| Medicina e Odontologia Legal | 30 | 18 | 12 | 0 |
| Nefropediatra | 30 | 0 | 30 | 0 |
| Neuropediatra | 30 | 0 | 30 | 0 |
| Oftalmologista | 30 | 0 | 30 | 0 |
| Pneumologista | 30 | 0 | 30 | 0 |
| Proctologista | 30 | 0 | 30 | 0 |
| Reumatologista | 30 | 0 | 30 | 0 |
| Socorrista | 30 | 0 | 30 | 0 |
| Administração Financeira | 29 | 29 | 0 | 0 |
| Bases Legais e Temas da Educação Nacional e Estadual | 29 | 29 | 0 | 0 |
| Comunicação Corporativa | 29 | 29 | 0 | 0 |
| Geotecnologias e Sistemas de Informação Geográfica (sig) | 29 | 29 | 0 | 0 |
| Geriatra | 29 | 0 | 29 | 0 |
| Mastologista | 29 | 0 | 29 | 0 |
| Programador | 29 | 29 | 0 | 0 |
| Psiquiatria da Infância e Adolescência | 29 | 29 | 0 | 0 |
| Ética e Conduta Pública | 29 | 29 | 0 | 0 |
| Análise de Informação | 28 | 16 | 12 | 0 |
| Bases Legais e Temas da Educação Nacional e Distrital | 28 | 28 | 0 | 0 |
| Gestão Ambiental | 28 | 19 | 9 | 0 |
| Nbr 9.077 | 28 | 28 | 0 | 0 |
| Programação, Controle e Acompanhamento de Obras | 28 | 27 | 1 | 0 |
| Saúde Mental | 28 | 28 | 0 | 0 |
| Trabalho | 28 | 0 | 28 | 0 |
| Análise de Informações | 27 | 27 | 0 | 0 |
| Biomedicina/ciências Biológicas | 27 | 27 | 0 | 0 |
| Cancerologia Cirúrgica | 27 | 27 | 0 | 0 |
| Cancerologia Clínica | 27 | 27 | 0 | 0 |
| Direito Agrário | 27 | 0 | 19 | 8 |
| Endocrinologia Pediátrica | 27 | 27 | 0 | 0 |
| Engenharia | 27 | 0 | 27 | 0 |
| Marketing e Comunicação Social | 27 | 27 | 0 | 0 |
| Normas, Fiscalização e Legislação | 27 | 27 | 0 | 0 |
| Operador de Rádio | 27 | 0 | 27 | 0 |
| Plano Diretor da Embrapa (apenas para os Cargos de Pesquisador, Analista e Técnico) | 27 | 27 | 0 | 0 |
| Cirurgia Cardiovascular | 26 | 26 | 0 | 0 |
| Cirurgia Geral | 26 | 26 | 0 | 0 |
| Cuidador | 26 | 26 | 0 | 0 |
| Direito Digital | 26 | 25 | 1 | 0 |
| Eletricidade | 26 | 23 | 3 | 0 |
| Especialista em Análise de Processos de Negócios Análise de Processos de Negócios | 26 | 26 | 0 | 0 |
| Linguagens e Tecnologias de Programação | 26 | 26 | 0 | 0 |
| Medicina Nuclear | 26 | 26 | 0 | 0 |
| Medicina de Urgência | 26 | 26 | 0 | 0 |
| Nefrologia Pediátrica | 26 | 26 | 0 | 0 |
| Neurologia Pediátrica | 26 | 26 | 0 | 0 |
| Nutrologia | 26 | 26 | 0 | 0 |
| Oftalmologia | 26 | 26 | 0 | 0 |
| Organização | 26 | 26 | 0 | 0 |
| Transformadores | 26 | 15 | 11 | 0 |
| Transplante de Medula Óssea | 26 | 26 | 0 | 0 |
| Clínico do Posto de Saúde da Família (psf) | 25 | 0 | 25 | 0 |
| Ecografia Vascular com Doppler | 25 | 25 | 0 | 0 |
| Estomaterapia | 25 | 25 | 0 | 0 |
| Guarda Civil Municipal | 25 | 25 | 0 | 0 |
| História do Estado de Alagoas | 25 | 25 | 0 | 0 |
| Hospitalar | 25 | 25 | 0 | 0 |
| Instalações Elétricas | 25 | 25 | 0 | 0 |
| Legislação Complementar | 25 | 22 | 3 | 0 |
| Legislação de Interesse da Atividade de Inteligência | 25 | 25 | 0 | 0 |
| Língua Francesa | 25 | 25 | 0 | 0 |
| Neurofisiologia Clínica | 25 | 25 | 0 | 0 |
| Noções de Biologia | 25 | 0 | 25 | 0 |
| Noções de Física | 25 | 0 | 25 | 0 |
| Programador de Computador | 25 | 0 | 25 | 0 |
| Sistemas Aeroespaciais | 25 | 25 | 0 | 0 |
| Arquitetura Arquitetura | 24 | 24 | 0 | 0 |
| Comercial | 24 | 24 | 0 | 0 |
| Dentística | 24 | 24 | 0 | 0 |
| Fundamentos em Ti | 24 | 18 | 1 | 5 |
| Física Física | 24 | 19 | 5 | 0 |
| Medicina do Adolescente | 24 | 24 | 0 | 0 |
| Políticas e Legislações da Educação | 24 | 0 | 24 | 0 |
| Processos de Negócio | 24 | 13 | 7 | 4 |
| Arquitetura Arquitetura e Urbanismo | 23 | 23 | 0 | 0 |
| Marketing | 23 | 23 | 0 | 0 |
| Medicina de Emergência | 23 | 23 | 0 | 0 |
| Métodos Quantitativos | 23 | 23 | 0 | 0 |
| Plataforma Básica | 23 | 23 | 0 | 0 |
| Processo | 23 | 23 | 0 | 0 |
| Serviços Gerais | 23 | 23 | 0 | 0 |
| Tecnologia de Pescado | 23 | 9 | 0 | 14 |
| Ciências Sociais | 22 | 22 | 0 | 0 |
| Criminologia e Noções de Criminalística | 22 | 22 | 0 | 0 |
| Normas Técnicas de Correspondência | 22 | 22 | 0 | 0 |
| Noções de Criminalística | 22 | 0 | 22 | 0 |
| Regulador | 22 | 0 | 22 | 0 |
| Regulação | 22 | 22 | 0 | 0 |
| Sistemas de Informação | 22 | 16 | 6 | 0 |
| Sociologia do Direito | 22 | 20 | 2 | 0 |
| Temas em Medicina, Medicina da Família e Saúde | 22 | 0 | 22 | 0 |
| Astronomia de Posição e Mecânica Celeste | 21 | 21 | 0 | 0 |
| Criminalística | 21 | 20 | 1 | 0 |
| Direito Sanitário | 21 | 21 | 0 | 0 |
| Direitos Difusos, Coletivos e Individuais Homogêneos e Direito Processual Coletivo | 21 | 0 | 21 | 0 |
| Engenharia Civil Engenharia Civil | 21 | 15 | 6 | 0 |
| Matemática Atuarial | 21 | 19 | 2 | 0 |
| Pesca | 21 | 8 | 10 | 3 |
| Planejamento e Mobilidade Urbana | 21 | 20 | 1 | 0 |
| Tópicos Avançados | 21 | 21 | 0 | 0 |
| Analista de Geotecnologia Noções Básicas de Cartografia | 20 | 20 | 0 | 0 |
| Arquitetura e Equipamentos de Segurança | 20 | 20 | 0 | 0 |
| Atividade de Inteligência | 20 | 20 | 0 | 0 |
| Bucomaxilofacial | 20 | 0 | 20 | 0 |
| Cirurgião Pediátrico | 20 | 0 | 20 | 0 |
| Cirurgião Plástico | 20 | 0 | 20 | 0 |
| Cirurgião Torácico | 20 | 0 | 20 | 0 |
| Cirurgião Vascular | 20 | 0 | 20 | 0 |
| Direito da Infância e Juventude | 20 | 14 | 6 | 0 |
| Endocrinologista Pediátrico | 20 | 0 | 20 | 0 |
| Engenheiro em Segurança do Trabalho | 20 | 0 | 20 | 0 |
| Especialista em Experiência do Usuário (ux) Experiência do Usuário (ux) | 20 | 20 | 0 | 0 |
| Especialista em Paciente Pcd | 20 | 0 | 20 | 0 |
| Estomatologista | 20 | 0 | 20 | 0 |
| Estômago e Intestino | 20 | 20 | 0 | 0 |
| Farmacêutico | 20 | 0 | 20 | 0 |
| Fisioterapeuta | 20 | 0 | 20 | 0 |
| Fonoaudiólogo | 20 | 0 | 20 | 0 |
| Fundamentos de Estratégia e Planejamento | 20 | 20 | 0 | 0 |
| Gastroenterologista Pediátrico | 20 | 0 | 20 | 0 |
| Gestão Datacenter | 20 | 20 | 0 | 0 |
| Gineco/obstetra | 20 | 0 | 20 | 0 |
| Hemodinâmica | 20 | 20 | 0 | 0 |
| História do Rio Grande do Norte | 20 | 17 | 3 | 0 |
| Intensivista Pediátrico | 20 | 0 | 20 | 0 |
| Legislação Federal | 20 | 20 | 0 | 0 |
| Medicina Intensiva Pediátrica | 20 | 20 | 0 | 0 |
| Médico do Trabalho | 20 | 0 | 20 | 0 |
| Nbr 17068 | 20 | 20 | 0 | 0 |
| Nefrologista Pediátrico | 20 | 0 | 20 | 0 |
| Neurocirurgião Pediátrico | 20 | 0 | 20 | 0 |
| Nocões de Engenharia Mecânica | 20 | 20 | 0 | 0 |
| Noções de Direito | 20 | 15 | 5 | 0 |
| Otorrinolaringologista | 20 | 0 | 20 | 0 |
| Protesista | 20 | 0 | 20 | 0 |
| Relações Internacionais | 20 | 20 | 0 | 0 |
| Temas Educacionais | 20 | 0 | 20 | 0 |
| Terapeuta Ocupacional | 20 | 0 | 20 | 0 |
| Técnico em Imobilização Ortopédica | 20 | 0 | 20 | 0 |
| Técnico em Laboratório | 20 | 0 | 20 | 0 |
| Técnico em Nutrição e Dietética | 20 | 0 | 20 | 0 |
| Ultrassonografista | 20 | 0 | 20 | 0 |
| Áudio e Vídeo | 20 | 20 | 0 | 0 |
| Analista Clínico | 19 | 0 | 19 | 0 |
| Cardiologia Pediátrica | 19 | 19 | 0 | 0 |
| Ciências Naturais | 19 | 19 | 0 | 0 |
| Departamento Penitenciário Nacional | 19 | 19 | 0 | 0 |
| Educação de Surdos, Surdez e Libras | 19 | 19 | 0 | 0 |
| Endodontista | 19 | 0 | 19 | 0 |
| Finanças (18) | 19 | 15 | 4 | 0 |
| Fisioterapeuta Especialista em Terapia Intensiva Neonatal e Pediátrica | 19 | 0 | 19 | 0 |
| Geografia Geral, do Brasil e de Alagoas | 19 | 19 | 0 | 0 |
| Infraestrutura Ferroviária | 19 | 19 | 0 | 0 |
| Intérprete de Língua Brasileira de Sinais | 19 | 0 | 19 | 0 |
| Legislações | 19 | 19 | 0 | 0 |
| Nutricionista | 19 | 0 | 19 | 0 |
| Odontopediatra | 19 | 0 | 19 | 0 |
| Patologia Clínica/ Medicina Laboratorial | 19 | 19 | 0 | 0 |
| Proteção de Dados e Privacidade | 19 | 19 | 0 | 0 |
| Técnico em Patologia | 19 | 0 | 19 | 0 |
| Técnico em Segurança do Trabalho | 19 | 0 | 19 | 0 |
| Cancerologia Pediátrica | 18 | 18 | 0 | 0 |
| Direito Urbanístico e Ambiental | 18 | 16 | 2 | 0 |
| Do Trabalho | 18 | 18 | 0 | 0 |
| Ecocardiografia | 18 | 18 | 0 | 0 |
| Letras/libras | 18 | 0 | 18 | 0 |
| Programação | 18 | 18 | 0 | 0 |
| Realidade Brasileira | 18 | 18 | 0 | 0 |
| Sistemas de Armazenamento de Dados | 18 | 18 | 0 | 0 |
| Transportes | 18 | 18 | 0 | 0 |
| Administração de Redes | 17 | 16 | 1 | 0 |
| Bioquímica | 17 | 17 | 0 | 0 |
| Dinâmica de Voo | 17 | 17 | 0 | 0 |
| Direito Processual | 17 | 17 | 0 | 0 |
| Em Recursos Minerais – Especialidade: Direito – Foco de Atuação Outorga e Cargo 22: Especialista em Recursos Minerais – Especialidade: Qualquer Área de Formação – Fiscalização e Distribuição de Receitas) | 17 | 17 | 0 | 0 |
| Endoscopia Respiratória | 17 | 17 | 0 | 0 |
| Estratégia e Planejamento | 17 | 17 | 0 | 0 |
| Infraestrutura de Aplicações | 17 | 17 | 0 | 0 |
| Legislação da Guarda Civil Municipal de Boa Vista/rr | 17 | 2 | 15 | 0 |
| Parte Geral | 17 | 17 | 0 | 0 |
| Segurança Institucional | 17 | 17 | 0 | 0 |
| Sistemas de Informação Geográfica | 17 | 17 | 0 | 0 |
| Técnicas de Comunicação | 17 | 17 | 0 | 0 |
| Análise, Desenho e Automação de Processos | 16 | 16 | 0 | 0 |
| Atuário Atuário | 16 | 16 | 0 | 0 |
| Fluência em Dados | 16 | 16 | 0 | 0 |
| História do Estado de Rondônia | 16 | 0 | 16 | 0 |
| Infraestrutura de Redes | 16 | 13 | 3 | 0 |
| Instalações Prediais | 16 | 16 | 0 | 0 |
| Manutenção Mecânica | 16 | 16 | 0 | 0 |
| Operador de Máquinas | 16 | 0 | 16 | 0 |
| Orientação, Acompanhamento e Readaptações Profissionais | 16 | 16 | 0 | 0 |
| Tecnologia dos Materiais | 16 | 16 | 0 | 0 |
| Teoria das Organizações | 16 | 16 | 0 | 0 |
| Ética | 16 | 16 | 0 | 0 |
| Agente de Endemias | 15 | 0 | 15 | 0 |
| Antropologia no Brasil | 15 | 2 | 13 | 0 |
| Atendimento Educacional Especializado (aee) | 15 | 0 | 15 | 0 |
| Cirurgião Dentista Bucomaxilofacial | 15 | 0 | 15 | 0 |
| Cirurgião Dentista Odontopediatria | 15 | 0 | 15 | 0 |
| Densitometria Óssea | 15 | 15 | 0 | 0 |
| Direitos Difusos e Coletivos | 15 | 9 | 6 | 0 |
| Engenharia Elétrica/engenharia Eletrônica | 15 | 0 | 15 | 0 |
| Gestão Patrimonial | 15 | 15 | 0 | 0 |
| Gestão por Processo | 15 | 15 | 0 | 0 |
| Governança e Planejamento | 15 | 15 | 0 | 0 |
| Integridade Pública | 15 | 15 | 0 | 0 |
| Legislações de Segurança e Proteção de Dados | 15 | 15 | 0 | 0 |
| Leitura | 15 | 15 | 0 | 0 |
| Medicina da Família e Comunidade | 15 | 15 | 0 | 0 |
| Medicina de Família | 15 | 11 | 4 | 0 |
| Noções de Análise de Dados | 15 | 15 | 0 | 0 |
| Noções de Controle Interno | 15 | 15 | 0 | 0 |
| Política Nacional de Meio Ambiente | 15 | 15 | 0 | 0 |
| Princípios de Telecomunicações | 15 | 15 | 0 | 0 |
| Processamento de Áudio/vídeo e Radiodifusão | 15 | 15 | 0 | 0 |
| Serviços de Verificação de Óbitos | 15 | 0 | 15 | 0 |
| Técnico Agropecuário | 15 | 0 | 15 | 0 |
| Arquitetura e Tecnologias de Sistemas de Informação | 14 | 14 | 0 | 0 |
| Cuidador Escolar | 14 | 0 | 14 | 0 |
| Desenho Técnico e Documentação | 14 | 14 | 0 | 0 |
| Endocrinologia e Metabologia | 14 | 14 | 0 | 0 |
| Ensino | 14 | 14 | 0 | 0 |
| Fundamentos de Computação | 14 | 14 | 0 | 0 |
| Geografia do Estado de Alagoas | 14 | 14 | 0 | 0 |
| Gestão de Servidores | 14 | 14 | 0 | 0 |
| Ginecologia e Obstetrícia | 14 | 14 | 0 | 0 |
| Infraestrutura de Tic | 14 | 14 | 0 | 0 |
| Jurídica | 14 | 14 | 0 | 0 |
| Navegação Aérea | 14 | 14 | 0 | 0 |
| Noções de Primeiros Socorros | 14 | 0 | 14 | 0 |
| Obras - Planejamento, Normas, Fiscalização e Legislação | 14 | 4 | 10 | 0 |
| Recursos Florestais | 14 | 14 | 0 | 0 |
| Sensoriamento Remoto | 14 | 14 | 0 | 0 |
| Soluções de Automação e Suporte à Decisão | 14 | 14 | 0 | 0 |
| Trânsito e Manutenção Veicular | 14 | 14 | 0 | 0 |
| Turismo | 14 | 0 | 14 | 0 |
| Visualização dos Dados em Plataforma Geoweb | 14 | 14 | 0 | 0 |
| Acessibilidade | 13 | 13 | 0 | 0 |
| Análise de Projetos | 13 | 0 | 13 | 0 |
| Biodiversidade, Zoologia, Botânica e História Natural | 13 | 13 | 0 | 0 |
| Bloco Biologia | 13 | 13 | 0 | 0 |
| Criminalística Aplicada | 13 | 0 | 13 | 0 |
| Direito Direito Regulatório | 13 | 13 | 0 | 0 |
| Ecologia, Conservacão e Manejo da Biodiversidade | 13 | 13 | 0 | 0 |
| Eletrônica Digital | 13 | 13 | 0 | 0 |
| Ensino Religioso Ciências da Religião | 13 | 0 | 13 | 0 |
| Geofísica Aplicada a Barragens | 13 | 13 | 0 | 0 |
| Gestão | 13 | 13 | 0 | 0 |
| Hematologia e Hemoterapia Pediátrica | 13 | 13 | 0 | 0 |
| Infraestrutura em Ti (17) | 13 | 13 | 0 | 0 |
| Libras Educação de Surdos, Surdez e Libras | 13 | 0 | 13 | 0 |
| Limnologia, Qualidade de Água e do Solo | 13 | 10 | 3 | 0 |
| Noções de Ciência da Computação | 13 | 13 | 0 | 0 |
| Pesquisa Científica | 13 | 13 | 0 | 0 |
| Planejamento Urbano | 13 | 13 | 0 | 0 |
| Política e Segurança | 13 | 13 | 0 | 0 |
| Ética e Conduta | 13 | 0 | 13 | 0 |
| Ética, Transparência e Responsabilidade Socioambiental no Serviço Público | 13 | 13 | 0 | 0 |
| Administração, Governança e Planejamento Administração | 12 | 12 | 0 | 0 |
| Agente Comunitário de Saúde | 12 | 0 | 12 | 0 |
| Análise e Avaliação de Projetos | 12 | 12 | 0 | 0 |
| Análise e Gestão de Crédito | 12 | 12 | 0 | 0 |
| Arquitetura Tecnológica | 12 | 12 | 0 | 0 |
| De Comunicação | 12 | 0 | 12 | 0 |
| Direito Público | 12 | 12 | 0 | 0 |
| Endoscopia Ginecológica | 12 | 12 | 0 | 0 |
| Gestão de Recursos Hídricos | 12 | 12 | 0 | 0 |
| Ictiologia | 12 | 8 | 4 | 0 |
| Imunologia | 12 | 12 | 0 | 0 |
| Legislação Extravagante | 12 | 2 | 10 | 0 |
| Legislação do Sistema de Aviação Civil | 12 | 12 | 0 | 0 |
| Manutenção de Edificações | 12 | 12 | 0 | 0 |
| Mecânica dos Sólidos | 12 | 12 | 0 | 0 |
| Normativos da Pdpj-br | 12 | 7 | 5 | 0 |
| Piano | 12 | 12 | 0 | 0 |
| Povos e Comunidades Tradicionais e Conservação da Biodiversidade | 12 | 12 | 0 | 0 |
| Provimento Geral da Corregedoria Aplicado aos Juízes e Ofícios Judiciais | 12 | 12 | 0 | 0 |
| Sistemas Computacionais Aplicados a Ciências da Vida | 12 | 12 | 0 | 0 |
| Teoria Geral do Direito e da Política | 12 | 0 | 12 | 0 |
| Teoria de Voo | 12 | 12 | 0 | 0 |
| Aplicação de Tecnologias | 11 | 11 | 0 | 0 |
| Arquitetura e Organização de Computadores | 11 | 11 | 0 | 0 |
| Boas Práticas de Fabricação (bpf) | 11 | 11 | 0 | 0 |
| Caracterização e Política Urbana do Município de Fortaleza | 11 | 11 | 0 | 0 |
| Comunicações Móveis | 11 | 11 | 0 | 0 |
| E-social para Órgãos Públicos | 11 | 11 | 0 | 0 |
| Educação, Ciência, Tecnologia e Inovação | 11 | 11 | 0 | 0 |
| Finanças Finanças | 11 | 11 | 0 | 0 |
| Fundamentos | 11 | 9 | 2 | 0 |
| Geografia Geral e do Brasil | 11 | 11 | 0 | 0 |
| Geografia do Brasil | 11 | 11 | 0 | 0 |
| Geoprocessamento e Sensoriamento Remoto | 11 | 0 | 11 | 0 |
| Infantil | 11 | 0 | 11 | 0 |
| Infraestrutura Hídrica | 11 | 10 | 1 | 0 |
| Iso 22301 | 11 | 11 | 0 | 0 |
| Legislação e Normas Técnicas | 11 | 11 | 0 | 0 |
| Noções de Pedologia | 11 | 6 | 5 | 0 |
| Qualidade de Dados | 11 | 11 | 0 | 0 |
| Saneamento Ambiental | 11 | 11 | 0 | 0 |
| Sistema Normativo Anticorrupção | 11 | 11 | 0 | 0 |
| Suporte à Plataforma Mainframe | 11 | 11 | 0 | 0 |
| Vendas | 11 | 11 | 0 | 0 |
| Analista Técnico Ii – Cientista de Dados Cientista de Dados | 10 | 0 | 10 | 0 |
| Aplicações | 10 | 10 | 0 | 0 |
| Apoio Especializado | 10 | 10 | 0 | 0 |
| Aspectos Históricos, Sociais, Geopolíticos e Ambientais da Região da Amazônia Legal | 10 | 10 | 0 | 0 |
| Auxiliar Escolar | 10 | 0 | 10 | 0 |
| Biodiversidade, Florestas e Direitos Animais | 10 | 10 | 0 | 0 |
| Bioeconomia | 10 | 3 | 7 | 0 |
| Cartografia Digital | 10 | 10 | 0 | 0 |
| Comercial Legislação | 10 | 10 | 0 | 0 |
| Convênios e Contratos de Repasse Relativos às Transferências de Recursos da União | 10 | 10 | 0 | 0 |
| De Saúde | 10 | 0 | 10 | 0 |
| Direito Municipal | 10 | 6 | 4 | 0 |
| Dispositivos Implantáveis | 10 | 10 | 0 | 0 |
| Espanhol | 10 | 10 | 0 | 0 |
| Estatuto da Oab e Código de Ética | 10 | 10 | 0 | 0 |
| Estruturas de Barramento para Disposição de Rejeitos | 10 | 10 | 0 | 0 |
| Fiscalização e Controle Sanitário | 10 | 10 | 0 | 0 |
| Fundamentos da Preservação do Patrimônio Cultural | 10 | 10 | 0 | 0 |
| Infância e Juventude | 10 | 10 | 0 | 0 |
| Ingestão de Dados | 10 | 10 | 0 | 0 |
| Legislação Aplicável a Ti | 10 | 10 | 0 | 0 |
| Legislação Local | 10 | 10 | 0 | 0 |
| Legislação Pertinente ao Policial Militar de Alagoas | 10 | 10 | 0 | 0 |
| Literatura | 10 | 9 | 1 | 0 |
| Mudança do Clima | 10 | 6 | 4 | 0 |
| Nbr 9050 | 10 | 10 | 0 | 0 |
| Normativos Específicos | 10 | 0 | 10 | 0 |
| Noções de Química | 10 | 6 | 4 | 0 |
| Noções de Teoria Geral do Processo | 10 | 10 | 0 | 0 |
| Orientações a Serviço | 10 | 9 | 1 | 0 |
| Políticas e Legislações Educacionais | 10 | 10 | 0 | 0 |
| Qualidade Ambiental | 10 | 8 | 2 | 0 |
| Qualidade da Água | 10 | 10 | 0 | 0 |
| Química, Toxicologia Forense, Farmacologia e Genética Forense | 10 | 0 | 10 | 0 |
| Recursos Hídricos e Meio Ambiente | 10 | 10 | 0 | 0 |
| Sistemas de Comunicação Digital | 10 | 10 | 0 | 0 |
| Tecnologias Educacionais e Competências Sócio-emocionais | 10 | 10 | 0 | 0 |
| Ética e Cidadania | 10 | 10 | 0 | 0 |
| Ética e Integridade | 10 | 10 | 0 | 0 |
| Armazenamento de Dados | 9 | 9 | 0 | 0 |
| Arte Arte | 9 | 0 | 9 | 0 |
| Atendimento | 9 | 9 | 0 | 0 |
| Biotecnologia | 9 | 9 | 0 | 0 |
| Crea). 13 Nbr 9050 | 9 | 9 | 0 | 0 |
| De Software | 9 | 9 | 0 | 0 |
| Geologia de Engenharia Aplicada | 9 | 9 | 0 | 0 |
| Gestão Corporativa de Aquisição de Bens e Serviços | 9 | 9 | 0 | 0 |
| Infraestrutura Obras - Planejamento, Normas, Fiscalização e Legislação | 9 | 9 | 0 | 0 |
| Medicina Paliativa | 9 | 9 | 0 | 0 |
| Noções de Fitossanidade | 9 | 3 | 6 | 0 |
| Noções de Gestão | 9 | 9 | 0 | 0 |
| Noções de Gestão Ambiental | 9 | 9 | 0 | 0 |
| Perícia e Elaboração de Relatórios Técnicos, Pareceres e Laudos Periciais. Princípios de Planejamento de Obras e Serviços | 9 | 9 | 0 | 0 |
| Primeiros Socorros | 9 | 9 | 0 | 0 |
| Processamento de Sinais e Imagens Médicas | 9 | 9 | 0 | 0 |
| Redes | 9 | 9 | 0 | 0 |
| Redes de Comunicação | 9 | 9 | 0 | 0 |
| Relações Econômicas Internacionais | 9 | 9 | 0 | 0 |
| Ética, Transparência e Controle Social | 9 | 9 | 0 | 0 |
| Auxiliar de Desenvolvimento Infantil | 8 | 0 | 8 | 0 |
| Auxiliar de Educador | 8 | 0 | 8 | 0 |
| Ciência e Análise de Dados | 8 | 8 | 0 | 0 |
| Custos | 8 | 8 | 0 | 0 |
| Código de Ética e Conduta e Integridade da Caesb | 8 | 0 | 8 | 0 |
| Dimensionamento, Provimento e Movimentação da Força de Trabalho | 8 | 8 | 0 | 0 |
| Direito da Infância e da Juventude | 8 | 0 | 8 | 0 |
| Econômica do Acre | 8 | 0 | 8 | 0 |
| Edificações | 8 | 3 | 5 | 0 |
| Engenharia Mecânica Ou Mecatrônica | 8 | 8 | 0 | 0 |
| Ferramentas Analytics | 8 | 8 | 0 | 0 |
| Filosofia Jurídica | 8 | 5 | 3 | 0 |
| Formulação e Gestão de Políticas, Planos, Programas e Projetos Públicos (estaduais, Setoriais e Territoriais) | 8 | 8 | 0 | 0 |
| Gerenciamento de Infraestrutura | 8 | 8 | 0 | 0 |
| Gestão de Produtos | 8 | 0 | 8 | 0 |
| Governança de Dados | 8 | 8 | 0 | 0 |
| Governança de Dados e Scripts | 8 | 8 | 0 | 0 |
| Instrumentos e Processos de Medição de Grandezas Físicas, Químicas e Biomédicas | 8 | 8 | 0 | 0 |
| Mercados Financeiros e de Capitais | 8 | 8 | 0 | 0 |
| Metodologia de Pesquisa (apenas para os Cargos de Pesquisador) | 8 | 8 | 0 | 0 |
| Noções de Engenharia Elétrica | 8 | 8 | 0 | 0 |
| Noções de Organização | 8 | 8 | 0 | 0 |
| Noções de Transporte Escolar | 8 | 0 | 8 | 0 |
| Noções dos Programas e dos Projetos Educacionais | 8 | 8 | 0 | 0 |
| Oncologia | 8 | 8 | 0 | 0 |
| Operador de Estação de Tratamento | 8 | 0 | 8 | 0 |
| Ouvidoria | 8 | 8 | 0 | 0 |
| Prevenção e Tratamento de Incidentes | 8 | 8 | 0 | 0 |
| Processo Judicial Eletrônico | 8 | 8 | 0 | 0 |
| Qualidade em Prestação de Serviços | 8 | 8 | 0 | 0 |
| Testes | 8 | 8 | 0 | 0 |
| Tratamento de Água | 8 | 0 | 8 | 0 |
| Violência Doméstica | 8 | 5 | 3 | 0 |
| Ética e Legislação (apenas para os Cargos de Pesquisador e Analista) | 8 | 8 | 0 | 0 |
| Antropologia e Patrimônio Cultural | 7 | 0 | 7 | 0 |
| Aspirante-a-ofical Bombeiro Militar Física | 7 | 7 | 0 | 0 |
| Avaliação de Riscos e Controles Internos | 7 | 7 | 0 | 0 |
| Conceitos de Rede Local | 7 | 7 | 0 | 0 |
| Código de Ética | 7 | 7 | 0 | 0 |
| Direito Educacional | 7 | 7 | 0 | 0 |
| Direito Institucional | 7 | 4 | 3 | 0 |
| Engenharia Química/bioquímica/química/química Industrial | 7 | 7 | 0 | 0 |
| Fígado e Vias Biliares | 7 | 7 | 0 | 0 |
| Geografia do Maranhão | 7 | 4 | 3 | 0 |
| Governança Organizacional | 7 | 7 | 0 | 0 |
| Inovação em Ti no Sistema Financeiro | 7 | 6 | 1 | 0 |
| Legislação Profissional | 7 | 7 | 0 | 0 |
| Medicina Geral | 7 | 7 | 0 | 0 |
| Noções de Legislação Extravagante | 7 | 7 | 0 | 0 |
| Noções dos Direitos das Pessoas com Deficiência | 7 | 0 | 7 | 0 |
| Oficial Criminal – Cargos 4 a 13 Criminalística | 7 | 0 | 7 | 0 |
| Planejamento de Voo | 7 | 7 | 0 | 0 |
| Plataforma Alta (mainframe) | 7 | 7 | 0 | 0 |
| Processamento de Dados | 7 | 7 | 0 | 0 |
| Regulamento Brasileiro da Aviação Civil | 7 | 7 | 0 | 0 |
| Abnt Nbr Iso/iec 27001 | 6 | 3 | 3 | 0 |
| Análise da Informação | 6 | 0 | 6 | 0 |
| Backup | 6 | 6 | 0 | 0 |
| Biologia Celular e Molecular e Biotecnologia | 6 | 6 | 0 | 0 |
| Biotecnologia de Microrganismos | 6 | 6 | 0 | 0 |
| Cadastro, Engenharia de Avaliações e Perícias | 6 | 6 | 0 | 0 |
| Captação de Recursos e Alianças com o Público e o Privado | 6 | 6 | 0 | 0 |
| Controladoria-geral do Estado | 6 | 6 | 0 | 0 |
| Criminalística Aplicada e Conhecimentos Específicos da Área de Formação em Biologia | 6 | 0 | 6 | 0 |
| De Saúde Ii | 6 | 0 | 6 | 0 |
| Direito Fundiário | 6 | 0 | 6 | 0 |
| Filosofia do Direito | 6 | 6 | 0 | 0 |
| Fisoterapia | 6 | 6 | 0 | 0 |
| Fundamentos de Proteção de Infraestruturas Críticas | 6 | 6 | 0 | 0 |
| Gestão de Manutenção Predial | 6 | 5 | 1 | 0 |
| Gestão em Ti (4) | 6 | 4 | 2 | 0 |
| Governança e Gestão de Tic | 6 | 0 | 6 | 0 |
| Hardware | 6 | 6 | 0 | 0 |
| Hidrologia e Hidráulica de Barragens | 6 | 6 | 0 | 0 |
| Incêndios Florestais | 6 | 6 | 0 | 0 |
| Inspeções | 6 | 4 | 2 | 0 |
| Legislação e Normas Sobre Barragens | 6 | 6 | 0 | 0 |
| Limites de Segurança de Impurezas, Produtos de Degradação e Contaminantes | 6 | 6 | 0 | 0 |
| Marco Legal da Ct&i | 6 | 6 | 0 | 0 |
| Mdm (master Date Manegement) | 6 | 6 | 0 | 0 |
| Mídias Digitais | 6 | 6 | 0 | 0 |
| Nuvem Computacional | 6 | 6 | 0 | 0 |
| Políticas de Segurança | 6 | 6 | 0 | 0 |
| Proteção da Atmosfera | 6 | 3 | 3 | 0 |
| Proteção da Fauna | 6 | 6 | 0 | 0 |
| Proteção de Recursos Pesqueiros | 6 | 6 | 0 | 0 |
| Redes de Telecomunicações | 6 | 6 | 0 | 0 |
| Sistemas Urbanos de Abastecimento de Água | 6 | 0 | 6 | 0 |
| Administração de Recursos na Cabine de Comando | 5 | 5 | 0 | 0 |
| Analista Técnico Ii – Proposição Parlamentar Proposições Legislativas | 5 | 0 | 5 | 0 |
| Associação Brasileira de Normas Técnicas. Abnt Nbr Iso 22301 | 5 | 0 | 5 | 0 |
| Automação | 5 | 5 | 0 | 0 |
| Bioestatística | 5 | 5 | 0 | 0 |
| Contratação de Bens e Serviços de Ti | 5 | 5 | 0 | 0 |
| Criminalística Aplicada e Conhecimentos Específicos da Área de Formação em Engenharia | 5 | 0 | 5 | 0 |
| Direito Judiciário | 5 | 0 | 5 | 0 |
| Direito Militar | 5 | 0 | 5 | 0 |
| Direito da Pessoa Idosa | 5 | 5 | 0 | 0 |
| Embriologia | 5 | 5 | 0 | 0 |
| Equipamentos Elétricos e Eletrônicos | 5 | 2 | 3 | 0 |
| Estruturas de Disposição de Rejeitos | 5 | 5 | 0 | 0 |
| Execução Financeira | 5 | 0 | 5 | 0 |
| Geopolítica | 5 | 5 | 0 | 0 |
| Gestão e Fiscalização de Contratos por Escopo Ou Continuados | 5 | 5 | 0 | 0 |
| Iso 14004 | 5 | 5 | 0 | 0 |
| Legislação Referente à Temática de Gênero, Raça e Etnia | 5 | 5 | 0 | 0 |
| Legislação de Interesse Institucional | 5 | 5 | 0 | 0 |
| Legislação de Saneamento | 5 | 0 | 5 | 0 |
| Mecânica dos Solos Aplicada | 5 | 5 | 0 | 0 |
| Medicina Legal e Conhecimentos Específicos da Área de Psiquiatria | 5 | 0 | 5 | 0 |
| Meteorologia Aeronáutica | 5 | 5 | 0 | 0 |
| Métodos de Pesquisa | 5 | 5 | 0 | 0 |
| Noções Sobre Direitos da Pessoa com Deficiência | 5 | 0 | 5 | 0 |
| Noções Sobre a Funpresp | 5 | 5 | 0 | 0 |
| Noções de Administração e Situações Gerenciais | 5 | 0 | 5 | 0 |
| Noções de Fotografia | 5 | 5 | 0 | 0 |
| Noções de Saneamento | 5 | 0 | 5 | 0 |
| Pavimentação e Terraplenagem | 5 | 5 | 0 | 0 |
| Perícias | 5 | 5 | 0 | 0 |
| Principais Ameaças e Formas de Ataque | 5 | 5 | 0 | 0 |
| Procedimentos Operacionais | 5 | 5 | 0 | 0 |
| Processos de Desenvolvimento e Sustentação de Software | 5 | 5 | 0 | 0 |
| Promoção da Segurança e Medicina do Trabalho e da Qualidade de Vida e Bem-estar no Trabalho | 5 | 5 | 0 | 0 |
| Radiocomunicações | 5 | 5 | 0 | 0 |
| Redes de Comunicação de Dados | 5 | 0 | 5 | 0 |
| Regras de Tráfego Aéreo | 5 | 5 | 0 | 0 |
| Regulação e Agências Reguladoras (exceto para os Cargos 11: Analista – Especialidade: Qualquer Área de Formação, Cargo 13: e Especialista em Recursos Minerais – Especialidade: Comunicação e Cargo 15: Especialista em Recursos Minerais – Especialidade: Direito – Foco de Atuação Outorga) | 5 | 5 | 0 | 0 |
| Segurança de Sistemas Móveis (mobile) | 5 | 5 | 0 | 0 |
| Sistemas Embarcados | 5 | 5 | 0 | 0 |
| Sistemas Hidráulicos de Saneamento | 5 | 5 | 0 | 0 |
| Tecnologia de Alimentos | 5 | 5 | 0 | 0 |
| Tecnologias e Arquitetura de Datacenter | 5 | 5 | 0 | 0 |
| Tecnologias e Atividades Espaciais | 5 | 0 | 5 | 0 |
| Teoria Musical | 5 | 0 | 5 | 0 |
| 2005. 4.2 Nbr Iso/iec 27001 | 4 | 4 | 0 | 0 |
| Abnt Nbr 9050 | 4 | 4 | 0 | 0 |
| Análise e Projeto Orientados a Objetos | 4 | 4 | 0 | 0 |
| Análise e Projeto de Sistemas | 4 | 0 | 4 | 0 |
| Bioinformática | 4 | 4 | 0 | 0 |
| Cerimonial e Protocolo | 4 | 0 | 4 | 0 |
| Controladoria Geral do Estado | 4 | 4 | 0 | 0 |
| Correição no Poder Executivo Estadual | 4 | 4 | 0 | 0 |
| Demonstrativos Fiscais | 4 | 0 | 4 | 0 |
| Direito do Idoso | 4 | 0 | 4 | 0 |
| Edificação | 4 | 4 | 0 | 0 |
| Educação Ambiental | 4 | 4 | 0 | 0 |
| Engenharia de Dados | 4 | 4 | 0 | 0 |
| Engenharia de Tráfego | 4 | 4 | 0 | 0 |
| Ensaios de Materiais | 4 | 4 | 0 | 0 |
| Estratégia | 4 | 0 | 4 | 0 |
| Estudos de Estabilidade | 4 | 4 | 0 | 0 |
| Fisiologia | 4 | 4 | 0 | 0 |
| Fundamentos e Bases Legais da Educação | 4 | 4 | 0 | 0 |
| Geografia do Estado de Rondônia | 4 | 0 | 4 | 0 |
| Geografia do Estado do Maranhão | 4 | 0 | 4 | 0 |
| Geografia e História de Mato Grosso | 4 | 0 | 4 | 0 |
| Gerência de Redes | 4 | 4 | 0 | 0 |
| Histologia | 4 | 4 | 0 | 0 |
| Historia Geral, do Brasil e de Alagoas | 4 | 4 | 0 | 0 |
| Infraestrutura e Segurança | 4 | 0 | 4 | 0 |
| Instrumentação | 4 | 4 | 0 | 0 |
| Instrumentação Geotécnica em Barragens | 4 | 4 | 0 | 0 |
| Língua Japonesa | 4 | 4 | 0 | 0 |
| Matemática (para os Cargos 1 e 2) | 4 | 0 | 4 | 0 |
| Meio Ambiente e Mudança do Clima, Biodiversidade, Florestas e Direitos Animais | 4 | 0 | 4 | 0 |
| Microbiologia | 4 | 4 | 0 | 0 |
| Monitoramento Ambiental | 4 | 4 | 0 | 0 |
| Noções de Ciência Política | 4 | 4 | 0 | 0 |
| Noções de Matemática | 4 | 0 | 4 | 0 |
| Obras | 4 | 4 | 0 | 0 |
| Operações Típicas de Instituições Financeiras | 4 | 4 | 0 | 0 |
| Ori- Entações a Serviço | 4 | 4 | 0 | 0 |
| Parasitologia | 4 | 4 | 0 | 0 |
| Planejamento e Orçamento Governamental | 4 | 0 | 4 | 0 |
| Plataforma Baixa | 4 | 4 | 0 | 0 |
| Radiação | 4 | 4 | 0 | 0 |
| Segurança de Aplicações | 4 | 4 | 0 | 0 |
| Sisnama | 4 | 4 | 0 | 0 |
| Sistemas Urbanos de Esgotos | 4 | 0 | 4 | 0 |
| Suporte Técnico | 4 | 4 | 0 | 0 |
| Testes de Penetração | 4 | 4 | 0 | 0 |
| Ti – Planejamento, Normas, Fiscalização e Legislação | 4 | 0 | 4 | 0 |
| Toxicologia | 4 | 4 | 0 | 0 |
| Urbanização | 4 | 4 | 0 | 0 |
| Virologia | 4 | 4 | 0 | 0 |
| Ética e Estatuto Jurídico da Magistratura Nacional | 4 | 0 | 4 | 0 |
| Ética e Legislação (apenas para os Cargos de Técnico) | 4 | 4 | 0 | 0 |
| Analista Técnico Ii – Cerimonial e Eventos Produção de Eventos (planejar, Organizar e Executar) | 3 | 0 | 3 | 0 |
| Análise de Artefatos Maliciosos | 3 | 3 | 0 | 0 |
| Análise de Negócios | 3 | 0 | 3 | 0 |
| Análise de Vulnerabilidades | 3 | 3 | 0 | 0 |
| Armazenamento | 3 | 0 | 3 | 0 |
| Avaliação de Imóveis | 3 | 3 | 0 | 0 |
| Biotecnologia Estrutural | 3 | 3 | 0 | 0 |
| Cep | 3 | 0 | 3 | 0 |
| Comércio Exterior | 3 | 3 | 0 | 0 |
| Controle Ambiental por Registro | 3 | 3 | 0 | 0 |
| Cooperação Internacional | 3 | 0 | 3 | 0 |
| Distrito Federal e Política para Mulheres | 3 | 0 | 3 | 0 |
| Enzimologia | 3 | 3 | 0 | 0 |
| Georgrafia do Brasil | 3 | 3 | 0 | 0 |
| Gestão de Produto | 3 | 3 | 0 | 0 |
| Gestão de Resíduos Sólidos e Substâncias Perigosas | 3 | 0 | 3 | 0 |
| Gestão de Tic | 3 | 0 | 3 | 0 |
| Grupo Direito Material Coletivo (difusos, Coletivos e Individuais Homogêneos) | 3 | 0 | 3 | 0 |
| História Geral, do Brasil e de Alagoas | 3 | 3 | 0 | 0 |
| História, Geografia e Conhecimentos Gerais de Aracaju e Sergipe | 3 | 3 | 0 | 0 |
| Infraestrutura Tecnológica | 3 | 0 | 3 | 0 |
| Infraestrutura em Tic | 3 | 3 | 0 | 0 |
| Instruções Técnicas do Cbm/ro e Legislação Contra Incêndio e Pânico/ro | 3 | 0 | 3 | 0 |
| Legislação (apenas para os Cargos de Especialista) | 3 | 3 | 0 | 0 |
| Legislação Geral e do Setor de Meio Ambiente | 3 | 0 | 3 | 0 |
| Microinformática | 3 | 3 | 0 | 0 |
| Normas Relativas à Pmto | 3 | 0 | 3 | 0 |
| Noções Gerais de Administração nos Órgãos de Controle, Política Institucional, Deontologia Jurídica e Formação Humanística | 3 | 3 | 0 | 0 |
| Noções de Combate a Incêndio | 3 | 0 | 3 | 0 |
| Noções de Criminologia | 3 | 0 | 3 | 0 |
| Noções de Higiene e Saúde Bucal e de Instrumentos e Equipamentos | 3 | 0 | 3 | 0 |
| Noções de Proteção, Controle, Monitoramento e Fiscalização Ambiental | 3 | 0 | 3 | 0 |
| Nuvem | 3 | 3 | 0 | 0 |
| Parâmetros Curriculares Nacionais do Ensino Médio | 3 | 0 | 3 | 0 |
| Poluição Sonora | 3 | 3 | 0 | 0 |
| Princípios Institucionais da Defensoria Pública | 3 | 3 | 0 | 0 |
| Princípios e Atribuições Institucionais da Defensoria Pública | 3 | 0 | 3 | 0 |
| Processamento Digital de Sinais | 3 | 3 | 0 | 0 |
| Processos de Negócios | 3 | 3 | 0 | 0 |
| Produção e Certificação de Produtos para a Saúde | 3 | 3 | 0 | 0 |
| Proteção de Recursos Genéticos | 3 | 3 | 0 | 0 |
| Realidade Brasileira Atual | 3 | 3 | 0 | 0 |
| Responsabilização Pela Prática de Atos Ilícitos | 3 | 0 | 3 | 0 |
| Revisão de Texto | 3 | 3 | 0 | 0 |
| Ruptura Hipótetica de Barragens | 3 | 3 | 0 | 0 |
| Segurança de Aplicações Web | 3 | 3 | 0 | 0 |
| Segurança de Barragens | 3 | 3 | 0 | 0 |
| Seguridade Relações Humanas | 3 | 3 | 0 | 0 |
| Sistema Gerenciador Web | 3 | 3 | 0 | 0 |
| Tabelionato de Notas | 3 | 0 | 3 | 0 |
| Tanatologia Forense | 3 | 0 | 3 | 0 |
| Teoria do Direito | 3 | 0 | 3 | 0 |
| Teoria e Técnica Circuitos Elétricos | 3 | 0 | 3 | 0 |
| Transparência Pública | 3 | 0 | 3 | 0 |
| Transparência e Confidencialidade | 3 | 3 | 0 | 0 |
| Tratamento de Dados | 3 | 3 | 0 | 0 |
| Tratamento de Esgoto | 3 | 0 | 3 | 0 |
| Analista Técnico Ii – Design Design | 2 | 0 | 2 | 0 |
| Análise de Sistema (suporte) | 2 | 0 | 2 | 0 |
| Análise e Gerenciamento de Riscos | 2 | 2 | 0 | 0 |
| Aplicações Financeiras) | 2 | 2 | 0 | 0 |
| Aspectos Geoeconômicos do Rio Grande do Norte | 2 | 0 | 2 | 0 |
| Atração, Seleção e Retenção de Talentos | 2 | 2 | 0 | 0 |
| Avaliação | 2 | 0 | 2 | 0 |
| Biomecânica e Controle Neuromotor | 2 | 2 | 0 | 0 |
| Comissário de Justiça da Infância, da Juventude e do Idoso | 2 | 0 | 2 | 0 |
| Conceitos Gerais | 2 | 2 | 0 | 0 |
| Contratações em Ti | 2 | 0 | 2 | 0 |
| Controle da Qualidade de Produtos | 2 | 2 | 0 | 0 |
| Direito Econômico e de Proteção ao Consumidor | 2 | 0 | 2 | 0 |
| História do Estado do Maranhão | 2 | 0 | 2 | 0 |
| Iso/iec 27002 | 2 | 2 | 0 | 0 |
| Legislacao Pertinente ao Policial Militar de Alagoas | 2 | 2 | 0 | 0 |
| Legislação Sobre Educação e Ciência, Tecnologia e Inovação | 2 | 0 | 2 | 0 |
| Legislação da Agu, Gestão de Conflitos e Governança | 2 | 0 | 2 | 0 |
| Legislação e Normas Específicas | 2 | 0 | 2 | 0 |
| Marketing Marketing | 2 | 2 | 0 | 0 |
| Matemática (apenas para os Cargos de Assistente) | 2 | 2 | 0 | 0 |
| Matemática Atuarial de Danos | 2 | 2 | 0 | 0 |
| Medicina Legal e Conhecimentos Específicos da Área de Patologia | 2 | 0 | 2 | 0 |
| Médico) | 2 | 0 | 2 | 0 |
| Normas Locais | 2 | 0 | 2 | 0 |
| Normativos da Plataforma Digital do Poder Judiciário – Pdpj-br | 2 | 0 | 2 | 0 |
| Noções Gerais de Direitos | 2 | 2 | 0 | 0 |
| Participação do Brasil em Organizações e Iniciativas Internacionais | 2 | 0 | 2 | 0 |
| Performance e Tuning | 2 | 0 | 2 | 0 |
| Princípios Institucionais e Legislação da Defensoria Pública | 2 | 0 | 2 | 0 |
| Processos de Cargos, Carreiras e Remuneração de Servidores | 2 | 2 | 0 | 0 |
| Produtos Eletromagnéticos | 2 | 2 | 0 | 0 |
| Produtos e Serviços da Apexbrasil (somente para Perfil 1 | 2 | 0 | 2 | 0 |
| Química do Carbono | 2 | 2 | 0 | 0 |
| Registros Públicos | 2 | 0 | 2 | 0 |
| Relações Humanas | 2 | 2 | 0 | 0 |
| Sistemas Distribuídos | 2 | 2 | 0 | 0 |
| Sistemas e Equipamentos de Aeronaves | 2 | 2 | 0 | 0 |
| Soluções | 2 | 2 | 0 | 0 |
| Tutela dos Interesses Difusos, Coletivos e Individuais Homogêneos (meio Ambiente, Patrimônio Cultural, Consumidor, Infância e Juventude, Patrimônio Público, Deficientes e Idosos) | 2 | 0 | 2 | 0 |
| 2022, Abnt Nbr Iso/iec 27005 | 1 | 0 | 1 | 0 |
| 23.2.2 Grupo Direito Digital | 1 | 0 | 1 | 0 |
| Analista Técnico Ii – Infraestrutura Rede Infraestrutura de Redes | 1 | 0 | 1 | 0 |
| Analista de Sistemas – Suporte de Ti) Tecnologia | 1 | 0 | 1 | 0 |
| Arquitetura de Desenvolvimento da Pdpj-br | 1 | 0 | 1 | 0 |
| Arquitetura de Desenvolvimento da Plataforma Digital do Poder Judiciário – Pdpj-br | 1 | 0 | 1 | 0 |
| Associação Brasileira de Normas Técnicas. Abnt Nbr Iso/iec 38500 | 1 | 0 | 1 | 0 |
| Criminalística e Criminologia | 1 | 0 | 1 | 0 |
| Demais Normativas Disponibilizadas na Internet) | 1 | 1 | 0 | 0 |
| Direito Adminitrativo | 1 | 0 | 1 | 0 |
| Direito Agrário e Urbanístico | 1 | 0 | 1 | 0 |
| Direito Urbanístico/ambiental | 1 | 0 | 1 | 0 |
| Direito das Execuções Penais | 1 | 0 | 1 | 0 |
| Direito de Pessoal | 1 | 0 | 1 | 0 |
| Engenharia Ambiental Bloco I | 1 | 0 | 1 | 0 |
| Engenharia Ambiental, Legal, de Avaliações e Planejamento | 1 | 0 | 1 | 0 |
| Estatuto dos Policiais Civis do Estado de Pernambuco | 1 | 0 | 1 | 0 |
| Geografia Mundial | 1 | 1 | 0 | 0 |
| Gestão e Governança | 1 | 0 | 1 | 0 |
| Governo Aberto | 1 | 0 | 1 | 0 |
| Informação | 1 | 0 | 1 | 0 |
| Legislação Organizacional da Defensoria Pública | 1 | 0 | 1 | 0 |
| Legislação dos Servidores Civis do Estado do Piauí | 1 | 0 | 1 | 0 |
| Matemática Atuarial de Pessoas | 1 | 1 | 0 | 0 |
| Nbr Iso/iec 27001 | 1 | 0 | 1 | 0 |
| Normas Pertinentes à Pmto | 1 | 0 | 1 | 0 |
| Normas de Segurança e Saúde do Trabalho | 1 | 0 | 1 | 0 |
| Noções Gerais de Direito e Formação Humanística Sociologia do Direito | 1 | 0 | 1 | 0 |
| Noções de Direito das Pessoas com Deficiência | 1 | 0 | 1 | 0 |
| Obras Hídricas e de Saneamento Básico | 1 | 0 | 1 | 0 |
| Obras de Edificações Especiais | 1 | 0 | 1 | 0 |
| Obras de Saneamento Básico | 1 | 0 | 1 | 0 |
| Odontologia Legal | 1 | 0 | 1 | 0 |
| Organização da Medicina Legal no Brasil | 1 | 0 | 1 | 0 |
| Planejamento, Gerenciamento, Fiscalização, Normas e Legislação de Obras e Serviços de Engenharia | 1 | 1 | 0 | 0 |
| Ponto 2 | 1 | 0 | 1 | 0 |
| Princípios Institucionais da Advocacia-geral da União | 1 | 0 | 1 | 0 |
| Química (somente para o Cargo 1) | 1 | 0 | 1 | 0 |
| Registro de Imóveis | 1 | 0 | 1 | 0 |
| Responsabilização de Pessoas Pela Prática de Atos Ilícitos | 1 | 1 | 0 | 0 |
| Segurança do Trabalho e Higiene | 1 | 0 | 1 | 0 |
| Serviços e Gerenciamento de Redes | 1 | 0 | 1 | 0 |
| Sistemas de Informações Geográficas | 1 | 1 | 0 | 0 |
| Tecnologias Emergentes | 1 | 0 | 1 | 0 |
| Tratados e Convenções Internacionais Sobre Espaço Exterior | 1 | 0 | 1 | 0 |
| Tutela dos Interesses Difusos, Coletivos e Individuais Homogêneos | 1 | 0 | 1 | 0 |
| Técnicas de Controle | 1 | 0 | 1 | 0 |
| Técnicas de Gestão Ambiental | 1 | 0 | 1 | 0 |
| Técnico de Manejo e Meio Ambiente | 1 | 0 | 1 | 0 |
| Xiii Laboratório Médico-legal | 1 | 0 | 1 | 0 |
| Ética Profissional | 1 | 0 | 1 | 0 |

### Blocos da prova

| Bloco | Questões | Com disciplina |
|---|---|---|
| especificos | 150324 | 98873 |
| objetiva | 30078 | 11901 |
| basicos | 15732 | 11419 |
| gerais | 11509 | 6172 |
| discursiva | 5177 | 173 |
| especializados | 3511 | 2360 |
| (sem título de bloco) | 1642 | 1148 |
| complementares | 1553 | 516 |

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
| ano | concurso sem ano identificável | 9 |
| classificacao | prova inferida só pelo nome do arquivo | 23 |
| classificacao | gabarito sem fase clara (preliminar/definitivo) | 8 |
| classificacao | gabarito sem fase clara (preliminar/definitivo); sem código de prova no nome (vínculo depende do texto do PDF) | 1 |
| crawl | API detalhe HTTP N | 34 |
| crawl | concurso de teste publicado na API; ignorado | 1 |
| disciplina | edital de abertura sem conteúdo programático legível | 37 |
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
