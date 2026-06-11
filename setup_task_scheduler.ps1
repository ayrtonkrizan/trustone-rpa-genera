# Script PowerShell para configurar Task Scheduler no Windows
# Execute como Administrador

$TaskName = "GenneraRPA_Daily"
$ExePath = "C:\RPA\GenneraRPA.exe"
$WorkingDir = "C:\RPA"
$Time = "08:00AM"

Write-Host "Configurando Task Scheduler para RPA Gennera..." -ForegroundColor Green

# Criar ação
$Action = New-ScheduledTaskAction -Execute $ExePath -WorkingDirectory $WorkingDir

# Criar trigger (diariamente às 08:00)
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# Configurações adicionais
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

# Criar principal (executar com privilégios mais altos)
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Registrar tarefa
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Automação diária de exportação do sistema Gennera" `
    -Force

Write-Host "`nTask Scheduler configurado com sucesso!" -ForegroundColor Green
Write-Host "Nome da tarefa: $TaskName" -ForegroundColor Cyan
Write-Host "Horário de execução: $Time (diariamente)" -ForegroundColor Cyan
Write-Host "Executável: $ExePath" -ForegroundColor Cyan
Write-Host "`nPara visualizar: abra Task Scheduler e procure por '$TaskName'" -ForegroundColor Yellow
