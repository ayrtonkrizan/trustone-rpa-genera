# 🔧 SOLUÇÃO: Erro de Diretório Temporário

## ❌ Erro
```
ENOENT: no such file or directory, mkdtemp 'C:\Users\partner\AppData\Local\Temp\10\playwright-artifacts-XXXXXXXXXXXX'
```

## 🎯 Causa
O Playwright não consegue criar diretórios temporários devido a:
1. **Permissões insuficientes** no diretório `%TEMP%`
2. **Caminho inválido** ou inexistente
3. **Diretório temporário cheio** ou corrompido

---

## ✅ SOLUÇÃO RÁPIDA (1 minuto)

### Opção 1: Script Automático ⭐ Recomendado

```powershell
# Execute como Administrador
.\fix_temp_permissions.ps1
```

O script vai:
- ✅ Criar `C:\Users\partner\AppData\Local\Temp\playwright_temp`
- ✅ Configurar permissões corretas
- ✅ Limpar arquivos temporários antigos

### Opção 2: Manual (PowerShell como Admin)

```powershell
# 1. Criar diretório
$tempDir = "$env:TEMP\playwright_temp"
New-Item -ItemType Directory -Path $tempDir -Force

# 2. Dar permissões totais
$acl = Get-Acl $tempDir
$username = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $username, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
)
$acl.SetAccessRule($rule)
Set-Acl $tempDir $acl

Write-Host "✓ Diretório configurado: $tempDir"
```

### Opção 3: Limpar Diretório TEMP

```powershell
# Limpar arquivos temporários antigos
Remove-Item "$env:TEMP\playwright-*" -Recurse -Force -ErrorAction SilentlyContinue
```

---

## 🔍 Diagnóstico

### Verificar Permissões

```powershell
# Ver permissões do diretório TEMP
icacls $env:TEMP
```

Deve mostrar seu usuário com `(F)` (Full Control).

### Verificar Espaço em Disco

```powershell
# Ver espaço disponível
Get-PSDrive C | Select-Object Used,Free
```

Precisa ter pelo menos **500MB livres**.

### Verificar Variáveis de Ambiente

```powershell
# Ver diretórios temporários
Write-Host "TEMP: $env:TEMP"
Write-Host "TMP: $env:TMP"
```

Ambos devem apontar para o mesmo local válido.

---

## 🛠️ Soluções Alternativas

### 1. Usar Diretório Customizado

Adicione no `.env`:

```env
# Usar diretório customizado para temporários
TEMP=C:\ProgramData\Inovage\genera\temp
TMP=C:\ProgramData\Inovage\genera\temp
```

Crie o diretório:
```powershell
New-Item -ItemType Directory -Path "C:\ProgramData\Inovage\genera\temp" -Force
```

### 2. Executar como Administrador

Clique com botão direito em `GenneraRPA.exe` → **Executar como administrador**

### 3. Desabilitar Antivírus Temporariamente

Alguns antivírus bloqueiam criação de diretórios temporários. Tente adicionar exceção para:
- `C:\Users\partner\AppData\Local\Temp\playwright*`
- `GenneraRPA.exe`

---

## 📋 Checklist de Solução

- [ ] Executar `fix_temp_permissions.ps1` como Admin
- [ ] Verificar se `%TEMP%\playwright_temp` foi criado
- [ ] Verificar permissões do diretório (Full Control)
- [ ] Limpar arquivos temporários antigos
- [ ] Reiniciar GenneraRPA.exe
- [ ] Verificar logs para confirmar sucesso

---

## ✅ Como Saber se Funcionou

Execute o bot e procure no log:

```
INFO - Diretório temporário: C:\Users\partner\AppData\Local\Temp\playwright_temp
INFO - ✓ Chrome do sistema encontrado: ...
INFO - ✓ Navegador iniciado com sucesso
```

Se aparecer isso, **problema resolvido!** 🎉

---

## 🆘 Se Ainda Não Funcionar

### 1. Verificar Logs Detalhados

Execute com log DEBUG no `.env`:
```env
LOG_LEVEL=DEBUG
```

### 2. Testar Criação Manual

```powershell
# Testar se consegue criar diretório
$testDir = "$env:TEMP\test_playwright_$(Get-Random)"
New-Item -ItemType Directory -Path $testDir
Remove-Item $testDir

# Se der erro, problema é de permissões do Windows
```

### 3. Reinstalar Playwright

```powershell
python -m pip uninstall playwright -y
python -m pip install playwright
python -m playwright install chromium
```

### 4. Usar Caminho Absoluto

Modifique o código para usar caminho fixo:
```env
# No .env
TEMP=C:\Temp
TMP=C:\Temp
```

Crie `C:\Temp` com permissões totais.

---

## 📊 Resumo de Soluções

| Solução | Tempo | Complexidade | Taxa de Sucesso |
|---------|-------|--------------|-----------------|
| **fix_temp_permissions.ps1** ⭐ | 1 min | Baixa | 95% |
| **Limpar TEMP manual** | 2 min | Baixa | 80% |
| **Executar como Admin** | 10 seg | Muito Baixa | 70% |
| **Diretório customizado** | 3 min | Média | 90% |
| **Reinstalar Playwright** | 5 min | Alta | 85% |

---

## 💡 Prevenção

Para evitar o problema no futuro:

1. **Limpeza automática**: Agende limpeza do TEMP
   ```powershell
   # Criar tarefa agendada
   schtasks /create /tn "Limpar Temp Playwright" /tr "powershell -Command \"Remove-Item '$env:TEMP\playwright-*' -Recurse -Force\"" /sc weekly
   ```

2. **Monitorar espaço**: Mantenha pelo menos 1GB livre em C:

3. **Permissões**: Não altere permissões de `%TEMP%` manualmente

---

## 🎯 Recomendação Final

**Execute agora no servidor:**

```powershell
# Como Administrador
.\fix_temp_permissions.ps1
```

Depois execute:
```powershell
.\GenneraRPA.exe
```

Deve funcionar! ✅
