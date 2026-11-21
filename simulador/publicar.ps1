<#
  Publica o simulador na Cloudflare (Windows / PowerShell).

  Primeira vez:      .\publicar.ps1
  Depois de ativar o Cloudflare Access no painel:
                     .\publicar.ps1 -ConfigurarAcesso
  Atualizar o banco: .\publicar.ps1   (depois de rodar crawl/download/extract/classify)
#>
param([switch]$ConfigurarAcesso)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$NOME_DB = 'simulador-cebraspe'

function Executar([string]$cmd) {
  Write-Host "> $cmd" -ForegroundColor Cyan
  Invoke-Expression $cmd
  if ($LASTEXITCODE -ne 0) { throw "Falhou: $cmd" }
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  throw 'Node.js não encontrado. Instale a versão LTS em https://nodejs.org e abra um novo PowerShell.'
}
if (-not (Test-Path node_modules)) { Executar 'npm install' }

# 1. Login na Cloudflare (abre o navegador só na primeira vez)
$quem = (npx wrangler whoami 2>&1 | Out-String)
if ($quem -match 'not authenticated') { Executar 'npx wrangler login' }

# 2. Banco D1 do histórico de respostas: cria na primeira vez e grava o id no wrangler.jsonc
$cfg = Get-Content wrangler.jsonc -Raw
if ($cfg -match 'COLOQUE_AQUI_O_ID_DO_D1') {
  $db = (npx wrangler d1 list --json | ConvertFrom-Json) | Where-Object { $_.name -eq $NOME_DB }
  if (-not $db) {
    Executar "npx wrangler d1 create $NOME_DB"
    $db = (npx wrangler d1 list --json | ConvertFrom-Json) | Where-Object { $_.name -eq $NOME_DB }
  }
  if (-not $db.uuid) { throw "Não achei o id do banco $NOME_DB." }
  $cfg = $cfg -replace 'COLOQUE_AQUI_O_ID_DO_D1', $db.uuid
  [IO.File]::WriteAllText("$PSScriptRoot\wrangler.jsonc", $cfg)
  Write-Host "Banco D1 $NOME_DB = $($db.uuid)" -ForegroundColor Green
}
Executar "npx wrangler d1 execute $NOME_DB --remote --file schema.sql -y"

# 3. Login restrito (Cloudflare Access): grava os valores como secrets do Worker
if ($ConfigurarAcesso) {
  Write-Host 'Cole os valores mostrados ao ativar o Cloudflare Access (ver README.md).' -ForegroundColor Yellow
  Executar 'npx wrangler secret put TEAM_DOMAIN'
  Executar 'npx wrangler secret put POLICY_AUD'
  Executar 'npx wrangler secret put EMAILS_PERMITIDOS'
}

# 4. Gera as questões e as imagens a partir de ..\data\cebraspe.db
$py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
Executar "$py exportar.py"

# 5. Publica (só os arquivos que mudaram são enviados)
Executar 'npx wrangler deploy'
Write-Host 'Pronto. Abra o endereço *.workers.dev mostrado acima.' -ForegroundColor Green
