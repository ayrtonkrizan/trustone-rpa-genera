# RPA Gennera - Automação de Exportação

Sistema de automação (RPA) para exportar dados do sistema Gennera automaticamente.

## 📋 Funcionalidades

- ✅ **100% via API** - Não depende de interface web
- ✅ Login automático via API REST
- ✅ **Modelo 5**: Descontos Aplicados e Previstos (arquivo único)
- ✅ **Modelo 1**: Faturas com loop anual (2023 até ano atual)
- ✅ Download automático de múltiplos arquivos
- ✅ Extração e renomeação automática
- ✅ Sobrescreve arquivos antigos automaticamente
- ✅ Logs detalhados de execução
- ✅ Compilável para executável único (.exe)
- ✅ Rápido e confiável (sem seletores CSS)

## � Arquivos Gerados

Após a execução, os seguintes arquivos serão criados na pasta de downloads:

```
downloads/
├── modelo-5.csv          # Descontos Aplicados e Previstos (sempre sobrescrito)
├── modelo-1_2023.csv     # Faturas de 2023 (sempre sobrescrito)
├── modelo-1_2024.csv     # Faturas de 2024 (sempre sobrescrito)
├── modelo-1_2025.csv     # Faturas de 2025 (sempre sobrescrito)
├── modelo-1_2026.csv     # Faturas de 2026 (sempre sobrescrito)
└── modelo-1.csv          # ⭐ CONSOLIDADO: Todas as faturas 2023-2026 (UTF-8)
```

**Notas**:
- Os arquivos são sobrescritos a cada execução, mantendo sempre os dados mais recentes
- `modelo-1.csv` é criado automaticamente consolidando todos os anos
- Encoding UTF-8 para suportar caracteres especiais (acentos, ç, etc.)
- Cabeçalho incluído apenas uma vez no arquivo consolidado
- Todos os arquivos em formato CSV

## �🚀 Desenvolvimento

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
cd rpa-gennera
```

2. Instale as dependências:
```bash

```

3. Instale os navegadores do Playwright:
```bash
playwright install chromium
```

4. Configure o arquivo `.env`:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### Executar em Desenvolvimento

```bash
python main.py
```

## 📦 Compilação para Executável Windows

### ⚠️ IMPORTANTE: Compilação Cross-Platform

Para gerar um `.exe` Windows, você **DEVE compilar em uma máquina Windows**. Não é possível gerar `.exe` a partir de macOS/Linux.

### Opção 1: Compilar em Máquina Windows (Recomendado)

1. **Copie o projeto** para uma máquina Windows
2. **Instale Python 3.9+** (https://www.python.org/downloads/)
3. **Abra o PowerShell/CMD** na pasta do projeto
4. **Execute**:

```bash
# Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Compilar
python build.py
```

O executável será gerado em `dist/GenneraRPA.exe` (~150MB).

### Opção 2: GitHub Actions (Automático)

Se você usar GitHub:

1. **Faça push** do código para o GitHub
2. O workflow `.github/workflows/build-windows.yml` será executado automaticamente
3. **Baixe o executável** em: `Actions → Build Windows Executable → Artifacts`

### Opção 3: Usar Máquina Virtual Windows

1. Instale VirtualBox ou VMware
2. Crie uma VM com Windows 10/11
3. Siga os passos da Opção 1 dentro da VM

### Estrutura de Deploy

Após compilar, você terá:
```
dist/
└── GenneraRPA.exe  (executável único para Windows)
```

## 🖥️ Deploy em Produção (Windows Server)

### ⚠️ IMPORTANTE: Instalação do Navegador

O executável precisa do Chromium para funcionar. Escolha uma opção:

#### **Opção A: Executável com Chromium Incluído** ⭐ Recomendado

Ao compilar no Windows, execute ANTES:
```bash
python -m playwright install chromium
python build.py  # Chromium será incluído automaticamente
```

Resultado: Executável maior (~300MB) mas totalmente portátil.

#### **Opção B: Instalar Chromium no Servidor**

1. Copie `install_browsers.ps1` para o servidor
2. Execute (botão direito → "Executar com PowerShell")
3. Aguarde download (~150MB)

Resultado: Executável menor (~30MB) mas precisa Python no servidor.

### 1. Preparar o Servidor

Crie a estrutura de pastas:
```powershell
mkdir C:\RPA
mkdir C:\RPA\Downloads
```

### 2. Copiar Arquivos

Copie para `C:\RPA\`:
- `GenneraRPA.exe` (da pasta dist/)
- `.env` (configurado com credenciais de produção)

### 3. Configurar o .env

Edite `C:\RPA\.env`:
```env
# Credenciais Gennera
GENNERA_USER=pwit@ligasolidaria.org.br
GENNERA_PASSWORD=pwit2024#
GENNERA_ID_USER=14383060

# Configurações
DOWNLOAD_FOLDER=C:\RPA\Downloads
INSTITUTION_ID=1134
MODEL_ID=5
MODEL_1_START_YEAR=2023

# Configurações do navegador
HEADLESS=true
TIMEOUT=30000

# Logs
LOG_LEVEL=INFO
LOG_FILE=C:\RPA\gennera_rpa.log
```

### 4. Testar Manualmente

```powershell
cd C:\RPA
.\GenneraRPA.exe
```

Verifique:
- ✅ Logs em `C:\RPA\gennera_rpa.log`
- ✅ Arquivos baixados em `C:\RPA\Downloads`

### 5. Configurar Agendamento Automático

Execute como **Administrador**:
```powershell
cd C:\RPA
.\setup_task_scheduler.ps1
```

Ou configure manualmente:

1. Abra **Task Scheduler** (Agendador de Tarefas)
2. Clique em **Create Basic Task** (Criar Tarefa Básica)
3. Configure:
   - **Nome**: GenneraRPA_Daily
   - **Trigger**: Daily (Diariamente) às 08:00
   - **Action**: Start a program (Iniciar programa)
   - **Program**: `C:\RPA\GenneraRPA.exe`
   - **Start in**: `C:\RPA`
4. Em **Settings** (Configurações):
   - ✅ Run whether user is logged on or not
   - ✅ Run with highest privileges
   - ✅ If task fails, restart every 10 minutes

## 📊 Monitoramento

### Verificar Logs

```powershell
Get-Content C:\RPA\gennera_rpa.log -Tail 50
```

### Verificar Última Execução

```powershell
Get-ScheduledTask -TaskName "GenneraRPA_Daily" | Get-ScheduledTaskInfo
```

### Verificar Arquivos Baixados

```powershell
Get-ChildItem C:\RPA\Downloads -Recurse
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente (.env)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `GENNERA_USER` | Email de login | - |
| `GENNERA_PASSWORD` | Senha de login | - |
| `GENNERA_ID_USER` | ID do usuário (necessário para API) | `14383060` |
| `DOWNLOAD_FOLDER` | Pasta de downloads | `./downloads` |
| `INSTITUTION_ID` | ID da instituição | `1134` |
| `MODEL_ID` | ID do modelo de exportação | `5` |
| `MODEL_1_START_YEAR` | Ano inicial para download do Modelo 1 | `2023` |
| `HEADLESS` | Executar sem interface gráfica | `true` |
| `TIMEOUT` | Timeout em milissegundos | `30000` |
| `LOG_LEVEL` | Nível de log (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `LOG_FILE` | Arquivo de log | `gennera_rpa.log` |

### Alterar Horário de Execução

Edite o script `setup_task_scheduler.ps1` e altere a linha:
```powershell
$Time = "08:00AM"  # Altere para o horário desejado
```

## 🐛 Troubleshooting

### Erro: "GENNERA_USER e GENNERA_PASSWORD devem estar configurados"
- Verifique se o arquivo `.env` está no mesmo diretório do executável
- Confirme que as variáveis estão preenchidas corretamente

### Erro: "Timeout waiting for selector"
- Aumente o valor de `TIMEOUT` no `.env`
- Verifique se o site está acessível
- Execute com `HEADLESS=false` para ver o que está acontecendo

### Download não inicia
- Verifique se a pasta `DOWNLOAD_FOLDER` existe e tem permissões de escrita
- Confirme que o `MODEL_ID` está correto

### Task Scheduler não executa
- Verifique se a tarefa está configurada para "Run with highest privileges"
- Confirme que o caminho do executável está correto
- Verifique os logs do Task Scheduler em Event Viewer

## 📝 Estrutura do Projeto

```
rpa-gennera/
├── main.py                      # Script principal
├── gennera_bot.py              # Lógica do bot
├── config.py                   # Configurações
├── build.py                    # Script de compilação
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de configuração
├── .gitignore                 # Arquivos ignorados pelo Git
├── setup_task_scheduler.ps1   # Script de agendamento Windows
└── README.md                  # Documentação
```

## 🔒 Segurança

- ⚠️ **NUNCA** commite o arquivo `.env` com credenciais reais
- ⚠️ Use permissões restritas na pasta `C:\RPA` em produção
- ⚠️ Mantenha os logs seguros (podem conter informações sensíveis)
- ✅ Considere usar Windows Credential Manager para senhas

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `gennera_rpa.log`
2. Execute com `HEADLESS=false` para debug visual
3. Aumente `LOG_LEVEL=DEBUG` para mais detalhes

## 📄 Licença

Uso interno - TrustOne / Liga Solidária
