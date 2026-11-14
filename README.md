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
- `extract` só reprocessa PDFs cujo SHA-256 (ou a versão do extrator) mudou; o vínculo prova↔gabarito é recalculado
  para os concursos alterados.

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
| `questao` | número, tipo (`CE`/`ME`/`DISC`), enunciado, alternativas (JSON), texto-base, seção, imagens, página, `origem_texto` |
| `gabarito` | preliminar, definitivo, anulada, alterada, justificativa, padrão de resposta e documentos de origem |
| `gabarito_bruto` / `gabarito_grupo` | respostas lidas de cada PDF de gabarito, antes do vínculo (reprocessável) |
| `justificativa_bruta` | linhas das tabelas de justificativas |
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
