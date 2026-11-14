# Relatório da Fase 0: Reconhecimento do site do Cebraspe

Data da coleta: 14/11/2026. Todas as requisições usaram User-Agent identificável, intervalo de no mínimo 1 s e retry com backoff exponencial.
Scripts usados: `cebraspe_bank/recon/scan_eventos.py` e `cebraspe_bank/recon/sample_download.py`.

## 1. Resumo

| Item | Resultado |
|---|---|
| Renderização | **SPA React**. O HTML de `/concursos/` vem vazio e o conteúdo chega por uma **API JSON pública**. Playwright não é necessário. |
| robots.txt | `www.cebraspe.org.br/robots.txt`: `User-agent: * / Disallow:` (tudo permitido). `apis.` e `cdn.` não têm robots.txt (404). |
| Concursos listados | **500** slugs únicos (501 entradas; `INSS_22` aparece duas vezes), com ano de 2014 a 2026. |
| Detalhe disponível | **466** concursos (93%). **34** retornam HTTP 500 em todas as tentativas (31 de 2015, 3 de 2014). |
| PDFs de interesse (sem as versões de acessibilidade) | ~**11.900**: 5.427 provas, 3.874 gabaritos definitivos, 286 preliminares, 453 justificativas e 1.856 padrões de resposta |
| Volume estimado em disco | ~**2,8 GB** (média de 233 KB por PDF na amostra de 18 arquivos) |
| Camada de texto | Presente em **18/18** PDFs da amostra (2016–2026). OCR deve ser exceção. |
| Site legado `cespe.unb.br` | **Inacessível**: TLS resetado na origem / 502. |

## 2. Estrutura do site e da API

### 2.1 Listagem
A página `https://www.cebraspe.org.br/concursos/` carrega `static/js/main.*.chunk.js`, que contém a configuração:

```
apiLink:   https://apis.cebraspe.org.br/cebraspe/
cdnLink:   https://cdn.cebraspe.org.br/
eventoURL: https://apis.cebraspe.org.br/cebraspe/eventos
```

| Rota do site | Endpoint JSON |
|---|---|
| `/concursos/` (todas as fases) | `GET /cebraspe/eventos/tipo/concursos/` |
| `/concursos/novos` | `GET /cebraspe/eventos/tipo/concursos/fase/novos` |
| `/concursos/inscricoes-abertas` | `.../fase/inscricoes-abertas` |
| `/concursos/em-andamento` | `.../fase/em-andamento` |
| `/concursos/encerrado` | `.../fase/encerrado` |
| `/concursos/{slug}` | `GET /cebraspe/eventos/{slug}` |

**Não há paginação.** O endpoint `/tipo/concursos/` devolve tudo de uma vez (≈250 KB), agrupado por fase: Novos 1, Inscrições Abertas 3, Em Andamento 69, Encerrados 428.
Campos da listagem: `eventoURL` (slug), `eventoNomeAbreviado`, `eventoAno`, `eventoStatus`, `eventoTotalVagas`, `eventoSalarioMaximo`.

### 2.2 Detalhe do concurso (`/eventos/{slug}`)
```
idEvento, eventoNomeAbreviado, eventoNomeCompleto, eventoAno, eventoStatus,
periodoInscricao ("De 22/12/2023 até 12/01/2024 ..."),
eventoCargos[]     {idArea, area}
arquivosEdital[]   {nomeArquivo, descricaoArquivo, dataArquivo, dataArquivoObj, tipoExtensaoArquivo, isGuid, isDataValid}
arquivosGabarito[] (mesma estrutura; apesar do nome, contém provas, gabaritos, padrões de resposta etc.)
```
- `arquivosGabarito` concentra **provas + gabaritos + padrões de resposta**.
- **Justificativas** ficam quase sempre em `arquivosEdital` (453 de ~460). Também há gabaritos soltos ali (562 descrições com "gabarito"). **O crawler precisa varrer as duas listas.**
- `dataArquivo` = data de publicação no site. Em concursos antigos aparece `01/01/0001` (`isDataValid=false`).
- 36 concursos não têm nenhum arquivo em `arquivosGabarito` (cancelados, em andamento ou sem prova).

### 2.3 Montagem da URL do arquivo (lógica `renderLink` do bundle)
```
isGuid == true                  -> https://cdn.cebraspe.org.br/{nomeArquivo}
tipoExtensaoArquivo=="_explorer" -> http://www.cespe.unb.br/concursos/{slug}/arquivos/{nomeArquivo}   (legado, fora do ar)
caso geral                      -> https://cdn.cebraspe.org.br/concursos/{slug}/arquivos/{nomeArquivo}
```
Na varredura: `isGuid=true` em 0 arquivos e `_explorer` em 1 arquivo (INSS_2015). Na prática, **tudo vem do CDN** no padrão geral. O `nomeArquivo` precisa ser URL-encoded, pois pode conter espaços, acentos e `–`.

## 3. CDN e nomes de arquivo

Host: `cdn.cebraspe.org.br` (Azion). Responde `application/pdf` sem autenticação. Listagem de diretório: 403 se a pasta existe, 404 se não existe.

Padrões de nome encontrados:

| Época | Prova | Gabarito | Observações |
|---|---|---|---|
| 2015–2016 | `234INSS_001_01_Caderno_LUA.PDF`, `291_SEEDF_007_01.pdf` | `Gab_Definitivo_234INSS_001_01.PDF` | Cadernos nomeados (LUA/MAR/NEVE, ALGA/BETA/CUBO) com sufixo `_01.._03` |
| 2017–2023 | `{cod}_{ORGAO}_{CB1\|CG1\|001}_{01}.PDF`; discursiva `{cod}_{ORGAO}_DISC_001.PDF` | `GAB_DEFINITIVO_{mesmo}.PDF`, `GAB_PRELIMINAR_{mesmo}.PDF` | `{cod}` = nº da prova (378, 670, 947…); `CB`/`CG` = conhecimentos básicos/gerais; `001` = específicos do cargo 1 |
| 2024 | `051_AEB_24_CB1_01.pdf`; `MATRIZ_039_CAESB_CG1_00_Com Justificativas_*.pdf` | `Gab_Definitivo_051_AEB_24_CB1_01.pdf` | Surgem os arquivos "prova + gabarito preliminar com justificativas" |
| 2025–2026 | **nome = hash SHA-256 hex** (`5B0C59…8A7100.pdf`) | idem | 6.026 arquivos com nome-hash. O tipo só pode ser inferido pela `descricaoArquivo` |

Sufixos de acessibilidade, que devem ser **ignorados** por serem duplicatas: `_ADAPTADA`, `_SUPER`/`SUPERAMPLIADA`, `_LEDOR`, `_TXT`, `BRAILLE`, VLibras (`.html`, `.mp4`). São ~2.500 arquivos.

Chave de vínculo prova ↔ gabarito: o **código no nome** (`947_CAPES_001_01`) aparece também no rodapé ou cabeçalho do gabarito, e o código de barras da prova traz `||234INSS_001_01N297373||`. Nos arquivos com nome-hash, esse vínculo precisa vir do **texto do PDF**, não do nome.

## 4. Onde está o ano

| Fonte | Onde | Cobertura / confiabilidade |
|---|---|---|
| `eventoAno` (API) | listagem e detalhe | 100% dos 500. Parece ser o ano do edital, mas em 14 casos diverge do upload do edital de abertura (ex.: `BCB_24`=2023, `SEDUC_AL_21`=2022) |
| **Cabeçalho do gabarito** | `EDITAL Nº 1 – CAPES, DE 14 DE DEZEMBRO DE 2023` + `Aplicação: 17/3/2024` | Dá **ano do edital e data de aplicação** no mesmo PDF. É a melhor fonte para `ano_edital` e `ano_aplicacao` |
| Cabeçalho da prova | 2019+: `CEBRASPE – CAPES – Edital: 2023`; até ~2017: `CESPE \| CEBRASPE – INSS – Aplicação: 2016` | O rótulo muda conforme a época ("Edital" vs. "Aplicação") e precisa ser lido com cuidado |
| Slug | `CAPES_23`, `INSS_2015`, `DPE_PE_14_DEFENSOR` | Ano no slug existe nos 500. Diverge do `eventoAno` em 20 casos |
| `dataArquivo` do "Edital nº 1 – Abertura" | detalhe | Data de **publicação no site**, que pode ser posterior ao edital. A busca por "Abertura" também pega editais de reabertura (ex.: SEE_16_DF "Edital nº 23 – Abertura") |
| `periodoInscricao` | detalhe | Período de inscrição, útil como sinal secundário |

**Proposta de precedência para `ano`** (cumpre a regra "data do edital > nome/slug > aplicação"):
1. `ano_edital` extraído do texto "EDITAL Nº … DE dd DE mês DE aaaa" (gabarito ou prova) → `ano_fonte='edital_pdf'`
2. ano do edital de abertura (data no nome ou no texto do edital, baixado só se necessário) → `'edital_abertura'`
3. ano no slug/nome → `'slug'`
4. `ano_aplicacao` (cabeçalho "Aplicação: d/m/aaaa") → `'aplicacao'`
5. sem fonte → `pendencia`

`eventoAno` da API fica gravado à parte, como evidência. Ponto para decidir: **ele deve entrar na cadeia de precedência?** Ele não é explicitamente "data do edital".

## 5. Amostra de layouts (18 PDFs, 8 concursos, 2016–2026)

| Concurso (ano) | Arquivo | Formato | Observações |
|---|---|---|---|
| INSS_2015 (aplic. 2016) | prova `Caderno_LUA` + gabarito | C/E, itens 1–120 | 3 cadernos (LUA/MAR/NEVE) por cargo com a **mesma numeração e itens em outra ordem** → o gabarito é por caderno. "Texto para os itens de 1 a 9". 1 página sem texto (capa). O código de barras gera lixo de texto (`Tfe_VT\`dVeq…`) que precisa ser filtrado |
| SEE_16_DF (2016) | prova 007 + gabarito | C/E, itens 71–120 | Os específicos começam no item 71: a numeração continua a dos básicos |
| ABIN_17 | CB1 + gabarito + padrão discursiva | C/E | Padrão de resposta com 23 páginas e imagens |
| TRE_BA_17 | justificativas | tabela `QUESTÃO / GAB. PRELIMINAR / GAB. DEFINITIVO / SITUAÇÃO` + texto | Situação: "Deferido com anulação" / "Deferido com alteração" (C→D). Organizado por prova/cargo |
| SEED_PR_20 | prova + gabarito | **Múltipla escolha A–E** ("Questão 1", alternativas `A`..`E`) | 81 imagens na prova. No gabarito aparecem `D X` / `A X X`: a marcação de anulada fica na mesma linha → **é preciso parsear por coordenadas** |
| TELEBRAS_21 | gabarito **preliminar** | C/E | Mesmo layout do definitivo, com o título "GABARITOS OFICIAIS PRELIMINARES" |
| CAPES_23 | prova 001 + definitivo + discursiva | C/E 51–120; discursiva com 1 questão | Gabarito traz edital, data de edital e aplicação. Itens anulados = `X` |
| CAESB_24 | prova (P1) + gabarito preliminar **com justificativas** | ME A–E, "Texto CG1A1" | 12 páginas, 44 imagens; versões "(ATUALIZADO)" e "(SEM EFEITO)" do mesmo documento |
| AGSUS_25_CCE | "PROVA E GABARITO DEFINITIVO" (nome-hash) | C/E em **formato novo** | Cada item: `1 B0703445 - CORRETO \| enunciado`. O comando se repete por item. Gabarito embutido (CORRETO/ERRADO). Numeração por bloco (`BLOCO II \| C1`) |

### Layout do gabarito padrão (2015–2024)
Grade de blocos de 20: uma linha de números e, abaixo, a linha de respostas (`C`/`E`/`A–E`/`X`). Células vazias saem como `0` no texto extraído. O cabeçalho traz órgão, nome do concurso, **edital nº/data**, **Aplicação**, código da prova (`947_CAPES_001_01`), cargo e, quando há, caderno ("CADERNO LUA"). Legenda: `( X ) item anulado`.
Com `get_text()` simples a ordem de leitura sai embaralhada. **O parse deve usar coordenadas** (`page.get_text("words")`/pdfplumber `extract_words`), alinhando colunas de número e resposta.

### Layout da prova
Duas colunas. O texto justificado vira uma palavra por linha no PyMuPDF (é preciso reflow). Marcadores: `-- CONHECIMENTOS BÁSICOS --`, `-- CONHECIMENTOS ESPECÍFICOS --`, `-- PROVA DISCURSIVA --` (bons para a Fase 5). Textos-base: "Texto para os itens de 1 a 9", "Texto CG1A1", "Julgue os itens a seguir…" (comando compartilhado). Itens C/E: número no início da linha. ME: "Questão N" + alternativas A–E.

## 6. Riscos e pendências

1. **34 concursos com API 500** (2014–2015): ANATEL_14, ANTAQ_14, DEPEN_15, DPE_PE_14_DEFENSOR, DPE_RN_15_DEFENSOR, DPF_14_AGENTE, DPU_15_ADMINISTRATIVO, FUB_15_1, FUNPRESP_15, MEC_15_TEMPORARIO, MPU_15, MP_15_ENAP, PREF_SALVADOR_15_PROCURADOR, SEC_BA_15_DIRETOR_E_VICE, SES_DF_15_MULTIPROFISSIONAL, SES_DF_15_MULTIPROFISSIONAL_2, SES_DF_15_RESIDENCIA, SES_DF_16_MULTIPROFISSIONAL, SES_DF_16_RESIDENCIA, STJ_15, TCE_PR_15_AUDITOR, TCE_RN_15_SERVIDOR, TCE_SC_15, TC_RN_15_AUDITOR, TELEBRAS_15, TJDFT_15_JUIZ, TJDFT_15_JUIZ_2, TJ_AM_15_JUIZ, TJ_PB_15_JUIZ, TRE_MT_15, TRE_PE_15, TRE_PI_15, TRE_RS_15, TRF1_15_JUIZ.
   As pastas existem no CDN (403 ≠ 404), mas sem a API não se sabe o nome dos arquivos, e o CDN não lista diretórios. O site legado `cespe.unb.br` está fora do ar. **Proposta:** registrar como `pendencia(etapa='crawl', motivo='API 500')` e tentar de novo a cada execução. Outra fonte possível seria um arquivo histórico (ex.: Wayback Machine), mas isso exige liberar um host novo e **depende da sua decisão**.
2. **Concursos anteriores a 2014 não estão listados.** O "mais antigo disponível" é 2014. O acervo antigo do Cespe/UnB não está acessível.
3. **Gabaritos preliminares quase sempre são removidos** depois do definitivo (só 286 restam). Na maioria dos concursos o "de→para" terá de vir das **justificativas** (453) ou dos arquivos "com justificativas" (2024+). Quando nenhum dos dois existir, `resposta_preliminar` fica NULL. Não será inferida.
4. **Nomes-hash (2025+)**: o tipo, o cargo e o caderno dependem só de `descricaoArquivo` e do texto do PDF. Isso aumenta os casos ambíguos que vão para revisão.
5. **Formatos mistos**: provas e gabaritos separados; "prova + gabarito definitivo" num só arquivo (2025+, formato `CORRETO/ERRADO` com código de item); "prova + gabarito preliminar com justificativas" (2024); versões "ATUALIZADO" / "SEM EFEITO" do mesmo documento. Isso pede regras de deduplicação e de versão.
6. **Numeração e caderno**: a numeração dos itens continua entre básicos e específicos (51–120) e pode mudar entre cadernos (LUA/MAR/NEVE). A chave do gabarito deve ser (concurso, código da prova/caderno, número), não só (cargo, número). Um mesmo arquivo de básicos serve a vários cargos ("CB2 – cargos 2, 3 e 10").
7. **Classificação por descrição** tem ruído: "Abertura" pega editais de reabertura, há erros de digitação ("CONEHCIMENTOS") e entidades HTML ("Aacute;REAS"). Precisa de normalização e de fila de revisão.
8. **API sem garantia**: endpoint não documentado, que pode mudar. Slug inexistente retorna HTTP 204 vazio (ex.: `TCU_19`), o que é diferente do erro 500. A resposta crua de cada execução deve ser guardada para auditoria.
9. **Imagens e fórmulas**: provas com dezenas de imagens (SEED_PR_20: 81). Precisam de recorte de região. Fórmulas costumam ser imagem ou fonte simbólica.

## 7. Estimativa de volume

| Item | Quantidade |
|---|---|
| Concursos listados | 500 (466 com detalhe, 34 pendentes) |
| Arquivos listados (todas as categorias) | 29.250 |
| Provas (objetivas + discursivas), sem acessibilidade | ~5.400 |
| Gabaritos definitivos / preliminares | ~3.900 / ~290 |
| Justificativas | ~450 |
| Padrões de resposta (discursivas) | ~1.850 |
| **Total a baixar (Fase 2)** | **~11.900 PDFs, ~2,8 GB** (com disco suficiente: 30 GB livres) |
| Tempo de download a 1 req/s | ~4–6 h (latência + tamanho), retomável |
| Questões (ordem de grandeza) | ~5.400 provas × ~60 itens ≈ **250–350 mil itens**, estimativa grosseira a validar na Fase 3 |

Arquivos por ano (`arquivosGabarito`): 2015: 165 · 2016: 1.248 · 2017: 823 · 2018: 928 · 2019: 391 · 2020: 626 · 2021: 996 · 2022: 922 · 2023: 1.359 · 2024: 2.312 · 2025: 1.272 · 2026: 935.

## 8. Ajustes propostos ao esquema

- `concurso`: acrescentar `ano_api` (o `eventoAno`), `id_evento`, `periodo_inscricao` e `json_bruto_sha256`.
- `documento`: acrescentar `descricao`, `lista_origem` (`edital`/`gabarito`), `data_publicacao`, `codigo_prova` (ex.: `947_CAPES_001_01`), `acessibilidade` (bool, para excluir) e `versao` (`atualizado`/`sem_efeito`). Ampliar `tipo` para incluir `padrao_resposta` e `prova_com_gabarito`.
- `prova`: acrescentar `codigo_prova`, `bloco` (`CB1`/`CG1`/`001`/`DISC`) e `cargos_aplicaveis` (um arquivo de básicos serve a vários cargos, por isso uma tabela `prova_cargo` N:N).
- `questao`: acrescentar `codigo_item` (ex.: `B0703445`, formato 2025+).
- `gabarito`: acrescentar `fonte_preliminar` e `fonte_definitiva` (documento_id).

## 9. Decisões que preciso de você antes da Fase 1

1. **34 concursos com API 500**: aceita registrar como pendência, ou quer que eu avalie uma fonte histórica (exige liberar `web.archive.org`)?
2. **`eventoAno` da API**: entra na cadeia de precedência do ano (ex.: antes do slug) ou fica só como evidência?
3. **Versões de acessibilidade** (adaptada, superampliada, ledor): confirmo que serão ignoradas?
4. **Ajustes de esquema da seção 8**: posso aplicar?
