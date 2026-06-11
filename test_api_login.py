import logging
from gennera_bot import GenneraBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_api_login():
    """Testa apenas o login via API"""
    logger.info("=== TESTE DE LOGIN VIA API ===")
    
    with GenneraBot() as bot:
        try:
            bot.setup()
            bot.login()
            
            logger.info("\n✓ Login via API funcionou!")
            logger.info("Aguardando 5 segundos para você verificar...")
            
            import time
            time.sleep(5)
            
            logger.info("\nTentando acessar página de exportações...")
            bot.navigate_to_exports()
            
            logger.info("\n✓ SUCESSO! Página de exportações carregada!")
            logger.info("Aguardando 10 segundos para você verificar...")
            time.sleep(10)
            
        except Exception as e:
            logger.error(f"✗ Erro: {e}", exc_info=True)

if __name__ == "__main__":
    test_api_login()
