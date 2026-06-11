import logging
import sys
from datetime import datetime
from pathlib import Path
from config import Config
from gennera_bot import GenneraBot

def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    
    logger.info("=" * 60)
    logger.info("INICIANDO RPA GENNERA")
    logger.info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        Config.validate()
        logger.info("Configurações validadas com sucesso")
        
        with GenneraBot() as bot:
            success = bot.run()
            
        if success:
            logger.info("Processo finalizado com sucesso")
            return 0
        else:
            logger.error("Processo finalizado com erros")
            return 1
            
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
