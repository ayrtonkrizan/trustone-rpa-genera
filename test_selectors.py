import logging
import time
from playwright.sync_api import sync_playwright
from config import Config

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_login_selectors():
    """Script para testar e descobrir os seletores corretos do formulário de login"""
    
    logger.info("Iniciando teste de seletores...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            logger.info(f"Acessando: {Config.GENNERA_LOGIN_URL}")
            page.goto(Config.GENNERA_LOGIN_URL)
            page.wait_for_load_state("networkidle")
            
            input("Pressione ENTER quando a página carregar completamente...")
            
            logger.info("\n=== ANALISANDO FORMULÁRIO ===")
            
            forms = page.query_selector_all('form')
            logger.info(f"Total de formulários encontrados: {len(forms)}")
            
            for i, form in enumerate(forms):
                logger.info(f"\n--- Formulário {i+1} ---")
                
                inputs = form.query_selector_all('input')
                logger.info(f"Total de inputs: {len(inputs)}")
                
                for j, inp in enumerate(inputs):
                    input_type = inp.get_attribute('type') or 'text'
                    input_name = inp.get_attribute('name') or 'N/A'
                    input_id = inp.get_attribute('id') or 'N/A'
                    input_ng_model = inp.get_attribute('ng-model') or 'N/A'
                    input_placeholder = inp.get_attribute('placeholder') or 'N/A'
                    
                    logger.info(f"\n  Input {j+1}:")
                    logger.info(f"    type: {input_type}")
                    logger.info(f"    name: {input_name}")
                    logger.info(f"    id: {input_id}")
                    logger.info(f"    ng-model: {input_ng_model}")
                    logger.info(f"    placeholder: {input_placeholder}")
                
                buttons = form.query_selector_all('button')
                logger.info(f"\nTotal de botões: {len(buttons)}")
                
                for k, btn in enumerate(buttons):
                    btn_type = btn.get_attribute('type') or 'button'
                    btn_text = btn.inner_text()
                    btn_class = btn.get_attribute('class') or 'N/A'
                    
                    logger.info(f"\n  Botão {k+1}:")
                    logger.info(f"    type: {btn_type}")
                    logger.info(f"    text: {btn_text}")
                    logger.info(f"    class: {btn_class}")
            
            logger.info("\n=== TESTANDO PREENCHIMENTO ===")
            
            input("\nPressione ENTER para testar preenchimento do email...")
            
            email_selectors = [
                'form input[type="email"]',
                'form input[name="username"]',
                'form input[ng-model*="username"]',
                'form input[ng-model*="email"]',
                'form input:first-of-type'
            ]
            
            for selector in email_selectors:
                try:
                    if page.is_visible(selector, timeout=1000):
                        logger.info(f"✓ Seletor de email ENCONTRADO: {selector}")
                        page.fill(selector, Config.GENNERA_USER)
                        logger.info(f"✓ Email preenchido com sucesso!")
                        break
                except Exception as e:
                    logger.info(f"✗ Seletor falhou: {selector} - {e}")
            
            logger.info("\n=== PROCURANDO BOTÃO PRÓXIMO ===")
            
            # Mostrar todos os botões disponíveis
            buttons = page.query_selector_all('form button')
            logger.info(f"Total de botões no formulário: {len(buttons)}")
            for i, btn in enumerate(buttons):
                btn_text = btn.inner_text().strip()
                btn_type = btn.get_attribute('type') or 'button'
                logger.info(f"  Botão {i+1}: '{btn_text}' (type={btn_type})")
            
            input("\nPressione ENTER para clicar no botão 'Próximo'...")
            
            # Tentar clicar por texto
            button_clicked = False
            for button in buttons:
                button_text = button.inner_text().strip().lower()
                if any(word in button_text for word in ['próximo', 'proximo', 'continuar', 'next']):
                    logger.info(f"✓ Botão ENCONTRADO com texto: '{button.inner_text().strip()}'")
                    button.click()
                    logger.info(f"✓ Botão clicado com sucesso!")
                    button_clicked = True
                    break
            
            if not button_clicked:
                logger.info("✗ Nenhum botão 'Próximo' encontrado, tentando primeiro botão...")
                if len(buttons) > 0:
                    buttons[0].click()
                    logger.info(f"✓ Primeiro botão clicado: '{buttons[0].inner_text().strip()}'")
            
            logger.info("\nAguardando próxima tela...")
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            logger.info("\n=== ANALISANDO FORMULÁRIO DE SENHA ===")
            
            forms = page.query_selector_all('form')
            logger.info(f"Total de formulários: {len(forms)}")
            
            for i, form in enumerate(forms):
                logger.info(f"\n--- Formulário {i+1} ---")
                inputs = form.query_selector_all('input')
                logger.info(f"Total de inputs: {len(inputs)}")
                
                for j, inp in enumerate(inputs):
                    input_type = inp.get_attribute('type') or 'text'
                    input_name = inp.get_attribute('name') or 'N/A'
                    input_ng_model = inp.get_attribute('ng-model') or 'N/A'
                    
                    logger.info(f"\n  Input {j+1}:")
                    logger.info(f"    type: {input_type}")
                    logger.info(f"    name: {input_name}")
                    logger.info(f"    ng-model: {input_ng_model}")
            
            input("\nPressione ENTER para testar preenchimento da senha...")
            
            password_selectors = [
                'form input[type="password"]',
                'form input[name="password"]',
                'form input[ng-model*="password"]',
                'form input[ng-model*="pass"]',
                'input[type="password"]'
            ]
            
            for selector in password_selectors:
                try:
                    if page.is_visible(selector, timeout=1000):
                        logger.info(f"✓ Seletor de senha ENCONTRADO: {selector}")
                        page.fill(selector, Config.GENNERA_PASSWORD)
                        logger.info(f"✓ Senha preenchida com sucesso!")
                        break
                except Exception as e:
                    logger.info(f"✗ Seletor falhou: {selector} - {e}")
            
            input("\nPressione ENTER para fechar o navegador...")
            
        except Exception as e:
            logger.error(f"Erro: {e}", exc_info=True)
        finally:
            browser.close()

if __name__ == "__main__":
    test_login_selectors()
