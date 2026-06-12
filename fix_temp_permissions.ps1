# Script para corrigir permissões do diretório temporário
# Execute este script se tiver erro: "ENOENT: no such file or directory, mkdtemp"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CORRIGINDO PERMISSÕES DE DIRETÓRIOS TEMPORÁRIOS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Criar diretório temporário do Playwright
$playwrightTemp = Join-Path $env:TEMP "playwright_temp"
Write-Host "Criando diretório: $playwrightTemp" -ForegroundColor Yellow

try {
    # Criar diretório se não existir
    if (-not (Test-Path $playwrightTemp)) {
        New-Item -ItemType Directory -Path $playwrightTemp -Force | Out-Null
        Write-Host "✓ Diretório criado" -ForegroundColor Green
    } else {
        Write-Host "✓ Diretório já existe" -ForegroundColor Green
    }
    
    # Dar permissões totais ao usuário atual
    $acl = Get-Acl $playwrightTemp
    $username = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $username,
        "FullControl",
        "ContainerInherit,ObjectInherit",
        "None",
        "Allow"
    )
    $acl.SetAccessRule($accessRule)
    Set-Acl $playwrightTemp $acl
    
    Write-Host "✓ Permissões configuradas para: $username" -ForegroundColor Green
    
} catch {
    Write-Host "ERRO ao configurar diretório: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente executar este script como Administrador" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# Limpar diretórios temporários antigos do Playwright
Write-Host "Limpando arquivos temporários antigos..." -ForegroundColor Yellow

try {
    $tempFiles = Get-ChildItem -Path $env:TEMP -Filter "playwright-*" -Directory -ErrorAction SilentlyContinue
    
    if ($tempFiles) {
        foreach ($file in $tempFiles) {
            try {
                Remove-Item $file.FullName -Recurse -Force -ErrorAction SilentlyContinue
                Write-Host "  ✓ Removido: $($file.Name)" -ForegroundColor Gray
            } catch {
                Write-Host "  ⚠ Não foi possível remover: $($file.Name)" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "  Nenhum arquivo temporário antigo encontrado" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "  ⚠ Erro ao limpar arquivos: $_" -ForegroundColor Yellow
}

Write-Host ""

# Verificar variáveis de ambiente
Write-Host "Verificando variáveis de ambiente..." -ForegroundColor Yellow
Write-Host "  TEMP: $env:TEMP" -ForegroundColor Gray
Write-Host "  TMP: $env:TMP" -ForegroundColor Gray

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "CORREÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Diretório configurado: $playwrightTemp" -ForegroundColor Cyan
Write-Host "Permissões: Controle Total para $username" -ForegroundColor Cyan
Write-Host ""
Write-Host "Agora você pode executar GenneraRPA.exe novamente" -ForegroundColor Green
Write-Host ""
Read-Host "Pressione Enter para sair"
