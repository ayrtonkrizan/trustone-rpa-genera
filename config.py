import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    GENNERA_LOGIN_URL = "https://apps.gennera.com.br/public/#/login"
    GENNERA_USER = os.getenv("GENNERA_USER")
    GENNERA_PASSWORD = os.getenv("GENNERA_PASSWORD")
    GENNERA_ID_USER = int(os.getenv("GENNERA_ID_USER", "14383060"))
    
    INSTITUTION_ID = os.getenv("INSTITUTION_ID", "1134")
    MODEL_ID = os.getenv("MODEL_ID", "5")
    EXPORTS_URL = f"https://financial.gennera.com.br/admin/#/institutions/{INSTITUTION_ID}/exports"
    
    # Ano inicial para download do modelo 1 (anual)
    MODEL_1_START_YEAR = int(os.getenv("MODEL_1_START_YEAR", "2023"))
    
    DOWNLOAD_FOLDER = Path(os.getenv("DOWNLOAD_FOLDER", "./downloads"))
    DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    CHROME_PATH = os.getenv("CHROME_PATH", "")  # Caminho customizado para Chrome (opcional)
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "gennera_rpa.log")
    
    @classmethod
    def validate(cls):
        if not cls.GENNERA_USER or not cls.GENNERA_PASSWORD:
            raise ValueError("GENNERA_USER e GENNERA_PASSWORD devem estar configurados no .env")
        if not cls.DOWNLOAD_FOLDER:
            raise ValueError("DOWNLOAD_FOLDER deve estar configurado no .env")
