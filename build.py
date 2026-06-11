import PyInstaller.__main__
import shutil
import platform
from pathlib import Path

def build():
    # Verificar sistema operacional
    current_os = platform.system()
    
    if current_os != "Windows":
        print("=" * 60)
        print("⚠️  AVISO: COMPILAÇÃO CROSS-PLATFORM")
        print("=" * 60)
        print(f"Sistema atual: {current_os}")
        print("Sistema alvo: Windows")
        print()
        print("IMPORTANTE:")
        print("- Você está compilando em {}, mas o executável será para Windows".format(current_os))
        print("- O .exe gerado pode NÃO funcionar corretamente")
        print("- Para melhor compatibilidade, compile em uma máquina Windows")
        print()
        print("Alternativas:")
        print("1. Use uma máquina Windows para compilar")
        print("2. Use GitHub Actions (veja .github/workflows/build-windows.yml)")
        print("3. Use uma VM Windows")
        print("=" * 60)
        
        # Em ambiente CI/CD, continuar automaticamente
        import os
        if not os.getenv('CI'):
            resposta = input("\nDeseja continuar mesmo assim? (s/N): ")
            if resposta.lower() != 's':
                print("Compilação cancelada.")
                return
        else:
            print("\nAmbiente CI/CD detectado, continuando automaticamente...")
        print()
    
    print("Iniciando compilação do executável...")
    
    # Detectar caminho dos browsers do Playwright
    import sys
    import os
    from pathlib import Path
    
    # Encontrar diretório de browsers do Playwright
    if current_os == "Windows":
        playwright_browsers = Path(os.environ.get('USERPROFILE', '')) / 'AppData' / 'Local' / 'ms-playwright'
    else:
        playwright_browsers = Path.home() / 'Library' / 'Caches' / 'ms-playwright'
    
    print(f"Procurando browsers Playwright em: {playwright_browsers}")
    
    # Preparar argumentos do PyInstaller
    pyinstaller_args = [
        'main.py',
        '--onefile',
        '--name=GenneraRPA',
        '--icon=NONE',
        '--clean',
        '--noconfirm',
        '--add-data=.env.example:.',
        '--hidden-import=playwright',
        '--hidden-import=dotenv',
        '--collect-all=playwright',
    ]
    
    # Adicionar browsers se existirem
    if playwright_browsers.exists():
        chromium_dir = None
        for browser_dir in playwright_browsers.iterdir():
            if browser_dir.is_dir() and 'chromium' in browser_dir.name.lower():
                chromium_dir = browser_dir
                break
        
        if chromium_dir:
            separator = ';' if current_os == "Windows" else ':'
            pyinstaller_args.append(f'--add-data={chromium_dir}{separator}playwright_browsers/chromium')
            print(f"✓ Chromium encontrado e será incluído: {chromium_dir.name}")
        else:
            print("⚠ Chromium não encontrado. Execute 'playwright install chromium' antes de compilar.")
    else:
        print("⚠ Diretório de browsers Playwright não encontrado.")
        print("   Execute 'playwright install chromium' antes de compilar.")
    
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n" + "="*60)
    print("COMPILAÇÃO CONCLUÍDA!")
    print("="*60)
    print(f"\nExecutável gerado em: dist/GenneraRPA.exe")
    print("\nPróximos passos:")
    print("1. Copie dist/GenneraRPA.exe para o servidor")
    print("2. Crie um arquivo .env no mesmo diretório do .exe")
    print("3. Configure as variáveis no .env (use .env.example como base)")
    print("4. Execute GenneraRPA.exe para testar")
    print("5. Configure o agendamento no Windows Task Scheduler")
    print("="*60)

if __name__ == "__main__":
    build()
