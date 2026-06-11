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
    
    PyInstaller.__main__.run([
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
    ])
    
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
