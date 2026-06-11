# Script para instalar browsers Playwright no Windows
# Execute este script ANTES de rodar o GenneraRPA.exe pela primeira vez

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "INSTALANDO BROWSERS PLAYWRIGHT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Host "ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.9+ de: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "Python encontrado: $($pythonCmd.Source)" -ForegroundColor Green
Write-Host ""

# Instalar Playwright
Write-Host "Instalando Playwright..." -ForegroundColor Yellow
python -m pip install --upgrade playwright

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO ao instalar Playwright!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "Playwright instalado com sucesso!" -ForegroundColor Green
Write-Host ""

# Instalar Chromium
Write-Host "Baixando Chromium (~150MB)..." -ForegroundColor Yellow
Write-Host "Isso pode levar alguns minutos..." -ForegroundColor Yellow
python -m playwright install chromium

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO ao instalar Chromium!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "INSTALAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Chromium instalado em:" -ForegroundColor Cyan
Write-Host "$env:USERPROFILE\AppData\Local\ms-playwright" -ForegroundColor White
Write-Host ""
Write-Host "Agora você pode executar GenneraRPA.exe" -ForegroundColor Green
Write-Host ""
Read-Host "Pressione Enter para sair"
