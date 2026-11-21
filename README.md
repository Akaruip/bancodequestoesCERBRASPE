# Banco local de questões do Cebraspe

Crawler e extrator que monta um banco SQLite com as questões (Certo/Errado, múltipla escolha e discursivas),
os textos-base, os gabaritos preliminares e definitivos, as justificativas de alteração/anulação e os padrões de
resposta publicados em <https://www.cebraspe.org.br/concursos/>.

**Uso exclusivamente pessoal, para estudo. Não redistribua o conteúdo baixado.** A pasta `data/` está no `.gitignore`.

## Requisitos

- Python 3.11+
- `pip install -r requirements.txt` (PyMuPDF, pdfplumber, requests)
- Tesseract com idioma português, para OCR de páginas sem texto: `apt-get install tesseract-ocr tesseract-ocr-por`
- Acesso de rede a `apis.cebraspe.org.br`, `cdn.cebraspe.org.br` e `www.cebraspe.org.br`

## Uso

```bash
python -m cebraspe_bank crawl                 # Fase 1: concursos e documentos (metadados)
python -m cebraspe_bank download              # Fase 2: PDFs de provas, gabaritos, justificativas e padrões
python -m cebraspe_bank extract               # Fases 3-4: questões, textos-base, imagens e gabaritos
python -m cebraspe_bank classify              # Fase 5: bloco, assunto e disciplina (regras, sem LLM)
python -m cebraspe_bank validate              # consistência + amostra de revisão (data/revisao/revisao_amostra.html)
python -m cebraspe_bank report                # REPORT_FINAL.md e data/pendencias.csv
```

Todos os comandos aceitam filtros:

| Flag | Efeito |
|---|---|
| `--concurso SLUG` | só esse concurso (repita a flag para vários). Ex.: `--concurso CAPES_23` |
| `--ano 2023` | só concursos daquele ano |
| `--desde 2020` | só concursos daquele ano em diante |
| `--db caminho.db` | outro arquivo de banco (padrão `data/cebraspe.db`) |
| `-v` | log detalhado |

Flags específicas: `crawl --refresh` (reconsulta também concursos encerrados), `download --limite N`
(no máximo N downloads nesta execução), `download --editais` (baixa também o edital de abertura de concursos cujo ano
veio só da data de publicação), `extract --refazer` (reprocessa PDFs já extraídos), `validate --amostra 20 --seed 42`.

Variáveis de ambiente: `CEBRASPE_DATA` (pasta de dados), `CEBRASPE_DB` (arquivo do banco).

## Atualização incremental

Basta rodar de novo, na mesma ordem:

```bash
python -m cebraspe_bank crawl && python -m cebraspe_bank download && python -m cebraspe_bank extract
```

- `crawl` lê a listagem (1 requisição) e só consulta o detalhe de concursos novos, não encerrados ou que falharam antes.
  Concursos encerrados já coletados são pulados (checkpoint `ok_encerrado`); use `--refresh` para forçar.
  Documentos que somem do site ficam marcados (`removido_do_site=1`), nunca apagados.
- `download` nunca baixa de novo um arquivo que já existe: confere o SHA-256 gravado. Arquivo presente sem registro é
  apenas registrado. Downloads são atômicos (`.part` → rename).
- `extract` só reprocessa PDFs cujo SHA-256 (ou a versão do extrator) mudou; o vínculo prova↔gabarito e a
  classificação por disciplina são recalculados para os concursos alterados.
- `classify` é idempotente: rode de novo (sem filtros) depois de editar as regras em `cebraspe_bank/disciplina.py`.

## Disciplina (Fase 5)

As provas do Cebraspe quase nunca trazem o nome da disciplina: os títulos são de bloco ("CONHECIMENTOS BÁSICOS",
"CONHECIMENTOS ESPECÍFICOS"). Por isso a classificação usa três colunas, cada uma com origem rastreável:

| Coluna | Conteúdo |
|---|---|
| `bloco` | bloco normalizado a partir do título lido no PDF: `basicos`, `gerais`, `especificos`, `complementares`, `especializados`, `discursiva`, `objetiva` (título genérico "PROVA OBJETIVA") |
| `assunto` | trecho **literal** do comando: "Acerca de **atos administrativos**, julgue…", "Julgue os itens, relativos a **taxas de juros**." No ME, a frase "assinale…" do enunciado. Trechos que só apontam para o contexto ("essa situação hipotética", "o texto CB1A1") são descartados |
| `disciplina` + `disciplina_fonte` | ver a precedência abaixo |
| `disciplina_edital` | nome da disciplina/área como está no edital (ou na prova, para `area_prova`) |

Precedência de `disciplina_fonte` (a primeira que se aplica vence):

1. `variante` — item de opção de língua estrangeira;
2. `titulo_pdf` — o título do bloco já é uma disciplina ("NOÇÕES DE INFORMÁTICA");
3. `regra_comando` — comando escrito em inglês/espanhol;
4. `edital_assunto` — **conteúdo programático do edital de abertura** (`cebraspe_bank/edital.py`): as candidatas são as
   disciplinas do edital para o cargo/área da prova e o mesmo grupo de bloco (básicos/gerais × específicos); o assunto
   literal é comparado (TF-IDF, sem LLM) com o nome e com cada tópico de cada candidata, e a 1ª precisa ter nota
   ≥ 1,5× a da 2ª;
5. `regra_assunto` — tabela de palavras-chave `REGRAS` (`cebraspe_bank/disciplina.py`) aplicada ao assunto;
6. `edital_unica` — o cargo/área tem uma única disciplina (ou só uma área) no edital, ex. "Engenharia Civil";
7. `area_prova` — concurso **sem conteúdo programático** (ex.: residências): a área declarada pela própria prova
   ("PROVA OBJETIVA - ÁREA PROFISSIONAL: NUTRIÇÃO"), só fora dos blocos básicos/gerais e se não for um rótulo genérico
   ("ÁREA: ADMINISTRATIVA").

A disciplina vinda do edital é padronizada pela tabela de regras quando possível ("NOÇÕES DE DIREITO ADMINISTRATIVO"
→ "Direito Administrativo"); senão fica o nome do edital ("Transportes Aquaviários"). O nome original fica em
`disciplina_edital`. Sem fonte, a disciplina fica NULL: nada é inferido pela posição do item ou por itens vizinhos.

Salvaguardas do edital: escolhe-se o edital "atualizado conforme retificações" ou o publicado por último (uma
republicação pode renumerar os cargos); prova sem cargo/área identificáveis cujas candidatas são de cargos diferentes
não é classificada pelo edital; disciplina cuja numeração de tópicos recomeça (engoliu outras cujos títulos não foram
lidos) não decide.

Conferência manual (amostras aleatórias): `regra_assunto` ≈ 95% de acerto; `edital_assunto` no banco inteiro, 37 de 40
corretas (2 erradas, 1 duvidosa). Para filtrar só o que veio do PDF, use `disciplina_fonte IN ('variante','titulo_pdf')`.

Os editais de abertura são baixados à parte (só eles, um PDF por concurso, o "atualizado conforme retificações"
quando houver) e lidos uma vez (cache em `edital_disciplina`):

```bash
python -m cebraspe_bank download --editais-conteudo
python -m cebraspe_bank classify
```

## Simulador na nuvem

A pasta [`simulador/`](simulador/README.md) publica um simulador de questões na Cloudflare (plano gratuito), com acesso
pelo celular e login restrito ao seu e-mail. O banco não sai do PC: `simulador/exportar.py` gera só os arquivos que o
simulador usa, e `simulador/publicar.ps1` envia. Passo a passo em [`simulador/README.md`](simulador/README.md).

## Regras de rede

- `robots.txt` respeitado (o do site permite tudo).
- No máximo **1 requisição por segundo**, somando todos os hosts, com User-Agent identificável.
- Retry com backoff exponencial (2, 4, 8, 16 s) para 429/5xx e erros de conexão; `Retry-After` respeitado.

## Ano do concurso

`concurso.ano` = ano do edital de abertura, pela precedência:

1. `edital_pdf` — "EDITAL Nº 1 – …, DE dd DE mês DE aaaa" lido no cabeçalho dos gabaritos
2. `edital_nome` — ano no nome do arquivo do Edital nº 1 de abertura (`ED_1_2023_…`)
3. `edital_publicacao` — data de publicação do Edital nº 1 de abertura no site
4. `slug` — ano no slug (`CAPES_23`)
5. `aplicacao` — data de aplicação da prova

A fonte usada fica em `ano_fonte`; `ano_edital` e `ano_aplicacao` ficam separados. O `eventoAno` da API fica em
`ano_api`, só como evidência. Concurso sem nenhuma fonte vai para `pendencia`; o ano nunca é estimado.

## Esquema (resumo)

| Tabela | Conteúdo |
|---|---|
| `concurso` | slug, órgão, nome, anos (e fontes), status, período de inscrição |
| `documento` | cada arquivo listado: tipo, modalidade, cargo, caderno, código da prova, URL, arquivo local, SHA-256 |
| `prova` / `prova_cargo` | um caderno de prova; um caderno de conhecimentos básicos serve a vários cargos (N:N) |
| `texto_base` | textos e comandos compartilhados, com faixa de itens quando informada ("itens de 1 a 9") |
| `questao` | número, `variante` (opção de língua estrangeira: `LÍNGUA INGLESA` etc.; vazio = item comum), tipo (`CE`/`ME`/`DISC`), enunciado, alternativas (JSON), `texto_base_id` (bloco imediatamente anterior: texto ou comando), `texto_id` (texto de apoio: o próprio bloco quando é texto, ou o texto citado pelo comando, ex. "do texto CB1A1"), seção, `bloco`, `assunto`, `disciplina` e `disciplina_fonte` (Fase 5), imagens, página, `origem_texto` |
| `gabarito` | preliminar, definitivo, anulada, alterada, justificativa, padrão de resposta e documentos de origem |
| `gabarito_bruto` / `gabarito_grupo` | respostas lidas de cada PDF de gabarito (por variante de língua, pela cor da célula e a legenda), antes do vínculo (reprocessável) |
| `justificativa_bruta` | linhas das tabelas de justificativas |
| `edital_disciplina` | conteúdo programático lido do edital de abertura: bloco, cargos, área, disciplina e tópicos (cache da Fase 5b) |
| `pendencia` | tudo o que não foi possível extrair/validar, com etapa e motivo |
| `checkpoint` | progresso por etapa (retomada) |
| `questao_fts` | busca textual (FTS5) em enunciado + texto-base |

Exemplo de busca:

```sql
SELECT q.id, c.slug, q.numero, g.resposta_definitiva
FROM questao_fts f JOIN questao q ON q.id = f.questao_id
JOIN prova p ON p.id = q.prova_id JOIN concurso c ON c.id = p.concurso_id
LEFT JOIN gabarito g ON g.questao_id = q.id
WHERE questao_fts MATCH 'improbidade AND dolo' LIMIT 20;
```

## Limitações conhecidas

Ver `REPORT_FASE0.md` (estrutura do site, riscos) e `REPORT_FINAL.md` (números e pendências). Em resumo:
34 concursos de 2014–2015 retornam erro 500 na API e ficam como pendência; não há concursos anteriores a 2014 no
site; gabaritos preliminares geralmente são retirados do site após o definitivo.

## Testes

```bash
python -m pytest -q tests
```
