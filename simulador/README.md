# Simulador na nuvem (Cloudflare, plano gratuito)

Site para responder as questões do banco pelo celular, 24h, sem o PC ligado. Só o(s) e-mail(s) autorizado(s)
entram: o login é feito pelo Cloudflare Access (código enviado por e-mail) e o Worker confere esse login em
**todo** pedido, inclusive nas imagens. Sem a configuração do Access, o site responde 403 para tudo.

## Como funciona

| Parte | Onde fica | Limite do plano gratuito |
|---|---|---|
| Questões, gabaritos, textos de apoio | arquivos estáticos do Worker (`public/dados/`), gerados por `exportar.py` | 20.000 arquivos por versão, 25 MiB cada |
| Imagens das questões | arquivos estáticos (`public/img/`), só as usadas | (mesmo limite) |
| Histórico de respostas | banco D1 `simulador-cebraspe` (tabela `resposta`) | 500 MB, 100 mil gravações/dia |
| Login | Cloudflare Access no endereço `*.workers.dev` | até 50 usuários |

O `cebraspe.db` não é enviado nem vai para o git: `exportar.py` lê o banco no seu PC e gera os arquivos que vão para
a Cloudflare. Na primeira exportação (2026-11-21) foram 219.526 questões em 2.196 blocos, 7.959 imagens, 10.156
arquivos e 418 MB. O índice `catalogo.json` (6 MB, ~0,6 MB comprimido) é baixado uma vez e os filtros e o sorteio
rodam no próprio navegador; cada questão vem do seu bloco de 100.

## Primeira publicação (Windows)

1. Instale o [Node.js LTS](https://nodejs.org) (o Python você já tem).
2. Crie uma conta gratuita em <https://dash.cloudflare.com/sign-up>.
3. Atualize o repositório (`git pull`) e, no PowerShell, dentro da pasta `simulador`:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\publicar.ps1
   ```

   O script instala o Wrangler, abre o navegador para você autorizar a Cloudflare, cria o banco D1, gera os
   arquivos e publica. No fim ele mostra o endereço, algo como `https://simulador-cebraspe.<sua-conta>.workers.dev`.
   Nesse momento o site ainda responde **403** (é o esperado: o login ainda não foi configurado).

4. Ative o login no painel da Cloudflare:
   1. **Workers & Pages** → `simulador-cebraspe` → **Settings** → **Domains & Routes**.
   2. Na linha `workers.dev`, clique em **Enable Cloudflare Access**. Se o Zero Trust ainda não estiver ativo, o painel
      pede para escolher um nome de time e o plano **Free**; depois volte a este passo.
   3. Anote os dois valores que aparecem: o **AUD tag** e o domínio do time (`https://<time>.cloudflareaccess.com`).
   4. Em **Manage Cloudflare Access**, deixe na política só o seu e-mail.
5. Grave esses valores no Worker e publique de novo:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\publicar.ps1 -ConfigurarAcesso
   ```

   Ele pergunta, um por vez: `TEAM_DOMAIN` (o domínio do time, com `https://`), `POLICY_AUD` (o AUD tag) e
   `EMAILS_PERMITIDOS` (seu e-mail; vários separados por vírgula).

6. Abra o endereço no celular, entre com o código que chega no e-mail e, no menu do navegador, use
   **Adicionar à tela inicial** para abrir como app.

## Atualizar as questões

Depois de rodar o crawler (`crawl`, `download`, `extract`, `classify`), na pasta `simulador`:

```powershell
powershell -ExecutionPolicy Bypass -File .\publicar.ps1
```

Só os arquivos que mudaram são enviados. O histórico de respostas é mantido (fica no D1, ligado ao id da questão).

## Testar no PC, sem login

```bash
cd simulador
npm install
python exportar.py                       # ou: python exportar.py --limite 2000 (amostra)
npx wrangler d1 execute simulador-cebraspe --local --file schema.sql
echo DEV_SEM_LOGIN=1 > .dev.vars         # só para o teste local; nunca vale na publicação
npx wrangler dev                         # http://localhost:8787
```

## Arquivos

- `exportar.py`: gera `public/dados/` e `public/img/` a partir de `data/cebraspe.db`.
- `src/worker.js`: confere o login (JWT do Cloudflare Access: assinatura, AUD, validade e e-mail) e serve os arquivos
  e a API de histórico (`GET /api/historico`, `POST /api/respostas`).
- `public/`: tela do simulador (HTML, CSS e JS sem dependências).
- `schema.sql`: tabela `resposta` do D1.
- `publicar.ps1`: publicação no Windows.

## O que o simulador mostra

- Filtros por disciplina, órgão, ano, tipo (C/E, ME, discursiva), bloco e histórico (todas, só novas, só as que errei).
  Anuladas ficam de fora, a não ser que você marque "Incluir anuladas".
- Gabarito definitivo; quando a prova só tem o preliminar, a tela avisa. Mostra também quando o gabarito foi alterado e
  a justificativa da banca, quando existe.
- Resultado com a nota líquida do Cebraspe para C/E (certas − erradas) e o placar de ME.
- Discursivas mostram o padrão de resposta da banca. Em algumas provas esse texto saiu ilegível na extração do PDF.
- Não há busca por texto livre: o índice de busca (FTS) tem 428 MB e ficou de fora para caber no plano gratuito.
