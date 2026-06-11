# ✅ SOLUÇÃO: Usar Chrome Instalado no Sistema

## Problema Resolvido
O executável agora **detecta e usa automaticamente** o Google Chrome instalado no Windows!

---

## 🎯 Como Funciona

O bot procura Chrome nesta ordem:

1. **Caminho customizado** (se definido no `.env`)
2. **Chrome do sistema** (locais padrão do Windows)
3. **Chromium empacotado** (se incluído no executável)
4. **Playwright padrão** (fallback)

---

## 🚀 Solução Imediata (NO SERVIDOR AGORA)

### Opção 1: Deixar Automático (Recomendado)

Baixe o novo executável do GitHub Actions e execute:

```bash
GenneraRPA.exe
```

O bot vai **encontrar automaticamente** o Chrome em:
- `C:\Program Files\Google\Chrome\Application\chrome.exe`
- `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- `%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe`

### Opção 2: Especificar Caminho Manualmente

Se o Chrome estiver em local diferente, adicione no `.env`:

```env
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

Ou o caminho onde seu Chrome está instalado.

---

## 📋 Locais Comuns do Chrome no Windows

```
C:\Program Files\Google\Chrome\Application\chrome.exe
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
%USERPROFILE%\AppData\Local\Google\Chrome\Application\chrome.exe
```

---

## 🔍 Como Encontrar o Caminho do Chrome

### Método 1: PowerShell
```powershell
Get-Command chrome | Select-Object -ExpandProperty Source
```

### Método 2: Atalho
1. Clique com botão direito no ícone do Chrome
2. Propriedades
3. Copie o caminho em "Destino"

### Método 3: Registro do Windows
```powershell
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe').'(default)'
```

---

## 📝 Exemplo de .env Completo

```env
# Credenciais
GENNERA_USER=pwit@ligasolidaria.org.br
GENNERA_PASSWORD=pwit2024#
GENNERA_ID_USER=14383060

# Configurações
DOWNLOAD_FOLDER=C:\ProgramData\Inovage\genera\downloads
INSTITUTION_ID=1134
MODEL_ID=5
MODEL_1_START_YEAR=2023

# Navegador
HEADLESS=true
TIMEOUT=60000
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

# Logs
LOG_LEVEL=INFO
LOG_FILE=C:\ProgramData\Inovage\genera\gennera_rpa.log
```

---

## ✅ Verificar se Funcionou

Execute o bot e procure no log:

```
✓ Chrome do sistema encontrado: C:\Program Files\Google\Chrome\Application\chrome.exe
Usando Google Chrome instalado no sistema
✓ Navegador iniciado com sucesso
```

---

## 🆘 Se Ainda Não Funcionar

### 1. Verificar se Chrome está instalado
```powershell
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

Deve retornar `True`.

### 2. Instalar Chrome
Se não estiver instalado: https://www.google.com/chrome/

### 3. Especificar caminho manualmente
Adicione `CHROME_PATH` no `.env` com o caminho correto.

### 4. Usar script de instalação do Playwright
```powershell
.\install_browsers.ps1
```

---

## 📊 Comparação de Soluções

| Solução | Tamanho .exe | Precisa Chrome? | Configuração |
|---------|--------------|-----------------|--------------|
| **Detecção Automática** ⭐ | ~30MB | ✅ Sim (já instalado) | Nenhuma |
| **CHROME_PATH manual** | ~30MB | ✅ Sim | Adicionar no .env |
| **Chromium empacotado** | ~300MB | ❌ Não | Recompilar |
| **install_browsers.ps1** | ~30MB | ❌ Não (instala) | Executar script |

---

## 🎯 Recomendação Final

**Use a detecção automática!**

1. Baixe novo executável do GitHub Actions
2. Execute `GenneraRPA.exe`
3. O bot vai encontrar o Chrome automaticamente

✅ Simples  
✅ Rápido  
✅ Funciona!
