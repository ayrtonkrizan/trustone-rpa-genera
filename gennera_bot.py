import logging
import time
import zipfile
import json
import base64
import csv
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Download
from config import Config

logger = logging.getLogger(__name__)

class GenneraBot:
    def __init__(self):
        self.config = Config
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def setup(self):
        logger.info("Iniciando navegador...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless= self.config.HEADLESS,
            args=['--start-maximized']
        )
        self.context = self.browser.new_context(
            viewport=None,
            accept_downloads=True
        )
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.TIMEOUT)
        logger.info("Navegador iniciado com sucesso")
    
    def login(self):
        logger.info("=== FAZENDO LOGIN VIA API ===")
        
        # Primeiro, visita a página inicial para obter cookies básicos
        logger.info("Acessando página inicial...")
        self.page.goto("https://apps.gennera.com.br/public/")
        self.page.wait_for_load_state("networkidle")
        time.sleep(1)
        
        # Preparar payload do login
        login_payload = {
            "username": self.config.GENNERA_USER,
            "idUser": self.config.GENNERA_ID_USER,
            "password": self.config.GENNERA_PASSWORD
        }
        
        logger.info(f"Enviando credenciais para API de login...")
        logger.info(f"Username: {self.config.GENNERA_USER}")
        
        # Fazer login via API usando evaluate (executa JavaScript no contexto da página)
        login_response = self.page.evaluate("""
            async (payload) => {
                const response = await fetch('https://apps.gennera.com.br/auth/login?nocache=' + Date.now(), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Accept': 'application/json, text/plain, */*'
                    },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                return {
                    status: response.status,
                    data: data
                };
            }
        """, login_payload)
        
        logger.info(f"Status da resposta: {login_response['status']}")
        
        if login_response['status'] == 200:
            logger.info("✓ Login via API realizado com sucesso!")
            
            # Extrair dados importantes
            user_data = login_response['data']
            token = user_data.get('token')
            user_hash = user_data.get('hash')
            id_user = user_data.get('idUser')
            
            logger.info(f"Token recebido: {token[:50]}...")
            logger.info(f"Hash: {user_hash}")
            logger.info(f"ID User: {id_user}")
            
            # Salvar token e dados do usuário no localStorage
            logger.info("Salvando token no localStorage...")
            self.page.evaluate(f"""
                localStorage.setItem('token', '{token}');
                localStorage.setItem('hash', '{user_hash}');
                localStorage.setItem('idUser', '{id_user}');
                localStorage.setItem('username', '{self.config.GENNERA_USER}');
                localStorage.setItem('userData', JSON.stringify({json.dumps(user_data)}));
            """)
            
            logger.info("✓ Token salvo no localStorage")
            
            # Aguardar um pouco para garantir que tudo foi salvo
            time.sleep(1)
            
            logger.info("✓ Autenticação concluída")
            
            # Retornar token para uso posterior
            return token
        else:
            error_msg = login_response.get('data', {}).get('message', 'Erro desconhecido')
            raise Exception(f"Falha no login via API: {error_msg}")
    
    def generate_export_model_5(self, token):
        """Gera URL de exportação do Modelo 5 (Descontos Aplicados e Previstos)"""
        logger.info("=== MODELO 5: Descontos Aplicados e Previstos ===")
        
        current_date = datetime.utcnow().isoformat() + "Z"
        institutions = [1134, 724, 727, 725, 726, 1051]
        
        params = {
            "institutions": institutions,
            "currentDate": current_date,
            "idStudent": None,
            "idItems": None,
            "discounts": None
        }
        
        params_json = json.dumps(params)
        params_base64 = base64.b64encode(params_json.encode()).decode()
        
        export_url = f"https://financial.gennera.com.br/institutions/{self.config.INSTITUTION_ID}/exports/5"
        export_url += f"?token={token}&params={params_base64}"
        
        logger.info(f"URL gerada para Modelo 5")
        return export_url
    
    def generate_export_model_1(self, token, year):
        """Gera URL de exportação do Modelo 1 (Faturas) para um ano específico"""
        logger.info(f"=== MODELO 1: Faturas - Ano {year} ===")
        
        current_date = datetime.utcnow().isoformat() + "Z"
        institutions = [1134, 724, 727, 725, 726, 1051]
        
        # Período: 01/01 até 31/12 do ano especificado
        cycle_start = f"{year}-01-01T03:00:00.000Z"
        cycle_end = f"{year}-12-31T03:00:00.000Z"
        
        params = {
            "institutions": institutions,
            "idStudent": None,
            "idFinancialResponsible": None,
            "cycleStart": cycle_start,
            "cycleEnd": cycle_end,
            "idItems": None,
            "paymentStatuses": None,
            "invoiceStatuses": ["open", "paid", "cancelled", "renegotiated", "loaned", "overdue", "underpaid", "overpaid"],
            "currentDate": current_date
        }
        
        params_json = json.dumps(params)
        params_base64 = base64.b64encode(params_json.encode()).decode()
        
        export_url = f"https://financial.gennera.com.br/institutions/{self.config.INSTITUTION_ID}/exports/1"
        export_url += f"?token={token}&params={params_base64}"
        
        logger.info(f"Período: {cycle_start} até {cycle_end}")
        logger.info(f"URL gerada para Modelo 1 - Ano {year}")
        return export_url
    
    def download_and_extract_zip(self, export_url, final_filename=None):
        """Baixa o arquivo ZIP diretamente da URL de exportação"""
        logger.info("Acessando URL de download...")
        
        # Navegar para a URL de exportação (isso iniciará o download)
        # Não esperar a página carregar pois o servidor aborta a navegação ao iniciar download
        with self.page.expect_download(timeout=120000) as download_info:
            try:
                self.page.goto(export_url, wait_until="commit")
            except Exception as e:
                # ERR_ABORTED é esperado quando o download inicia
                logger.debug(f"Navegação abortada (esperado): {e}")
        
        download: Download = download_info.value
        logger.info(f"✓ Download iniciado: {download.suggested_filename}")
        
        # Salvar arquivo temporário
        temp_filename = download.suggested_filename or "temp_export.zip"
        temp_path = self.config.DOWNLOAD_FOLDER / temp_filename
        download.save_as(temp_path)
        logger.info(f"✓ Arquivo salvo temporariamente")
        
        # Verificar se é um arquivo ZIP válido
        try:
            # Tentar abrir como ZIP
            logger.info("Extraindo arquivo ZIP...")
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                extracted_files = zip_ref.namelist()
                
                # Se temos um nome final específico, extrair e renomear
                if final_filename:
                    # Extrair primeiro arquivo do ZIP
                    first_file = extracted_files[0]
                    zip_ref.extract(first_file, self.config.DOWNLOAD_FOLDER)
                    
                    # Renomear para o nome final desejado
                    old_path = self.config.DOWNLOAD_FOLDER / first_file
                    new_path = self.config.DOWNLOAD_FOLDER / final_filename
                    
                    # Sobrescrever se já existir
                    if new_path.exists():
                        new_path.unlink()
                        logger.info(f"Arquivo antigo removido: {final_filename}")
                    
                    old_path.rename(new_path)
                    logger.info(f"✓ Arquivo renomeado para: {final_filename}")
                    extracted_files = [final_filename]
                else:
                    # Extrair normalmente sem renomear
                    zip_ref.extractall(self.config.DOWNLOAD_FOLDER)
                    logger.info(f"✓ Arquivos extraídos: {', '.join(extracted_files)}")
            
            # Remover arquivo temporário
            logger.info("Removendo arquivo temporário...")
            temp_path.unlink()
            logger.info("✓ Arquivo temporário removido")
            
            return extracted_files
            
        except zipfile.BadZipFile:
            # Não é um ZIP - provavelmente um CSV direto ou sem dados
            logger.warning(f"⚠ Arquivo não é ZIP (provavelmente sem dados para este período)")
            
            # Verificar se é um CSV direto
            if temp_filename.endswith('.csv'):
                logger.info("Arquivo CSV detectado, usando diretamente...")
                
                if final_filename:
                    # Renomear para o nome final
                    new_path = self.config.DOWNLOAD_FOLDER / final_filename
                    
                    if new_path.exists():
                        new_path.unlink()
                        logger.info(f"Arquivo antigo removido: {final_filename}")
                    
                    temp_path.rename(new_path)
                    logger.info(f"✓ Arquivo renomeado para: {final_filename}")
                    return [final_filename]
                else:
                    logger.info(f"✓ Arquivo mantido: {temp_filename}")
                    return [temp_filename]
            else:
                # Remover arquivo inválido
                temp_path.unlink()
                logger.warning(f"✗ Arquivo removido (formato inválido ou sem dados)")
                return []
    
    def consolidate_model_1_files(self, model_1_files):
        """Consolida todos os arquivos do Modelo 1 em um único CSV"""
        logger.info("\n" + "=" * 60)
        logger.info("CONSOLIDANDO ARQUIVOS DO MODELO 1")
        logger.info("=" * 60)
        
        consolidated_file = self.config.DOWNLOAD_FOLDER / "modelo-1.csv"
        all_rows = []
        header = None
        
        # Ordenar arquivos por ano para manter ordem cronológica
        sorted_files = sorted(model_1_files)
        
        for filename in sorted_files:
            file_path = self.config.DOWNLOAD_FOLDER / filename
            logger.info(f"Lendo: {filename}")
            
            try:
                # Ler arquivo CSV com encoding UTF-8
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    
                    if not rows:
                        logger.warning(f"Arquivo vazio: {filename}")
                        continue
                    
                    # Capturar cabeçalho do primeiro arquivo
                    if header is None:
                        header = rows[0]
                        logger.info(f"Cabeçalho capturado: {len(header)} colunas")
                        all_rows.append(header)
                    
                    # Adicionar dados (pular cabeçalho)
                    data_rows = rows[1:] if len(rows) > 1 else []
                    all_rows.extend(data_rows)
                    logger.info(f"  ✓ {len(data_rows)} linhas adicionadas")
                    
            except Exception as e:
                logger.error(f"Erro ao ler {filename}: {e}")
                continue
        
        # Escrever arquivo consolidado
        logger.info(f"\nEscrevendo arquivo consolidado...")
        with open(consolidated_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(all_rows)
        
        total_data_rows = len(all_rows) - 1  # Menos o cabeçalho
        logger.info(f"✓ Arquivo consolidado criado: modelo-1.csv")
        logger.info(f"✓ Total de linhas (sem cabeçalho): {total_data_rows}")
        logger.info(f"✓ Encoding: UTF-8")
        logger.info("=" * 60)
        
        return consolidated_file
    
    def run(self):
        try:
            self.setup()
            
            # Fazer login e obter token
            token = self.login()
            
            all_extracted_files = []
            
            # ===== MODELO 5: Descontos Aplicados e Previstos =====
            logger.info("\n" + "=" * 60)
            logger.info("BAIXANDO MODELO 5")
            logger.info("=" * 60)
            
            export_url_5 = self.generate_export_model_5(token)
            files_5 = self.download_and_extract_zip(export_url_5, final_filename="modelo-5.csv")
            all_extracted_files.extend(files_5)
            
            logger.info(f"✓ Modelo 5 salvo como: modelo-5.csv")
            
            # ===== MODELO 1: Faturas (Loop Anual) =====
            logger.info("\n" + "=" * 60)
            logger.info("BAIXANDO MODELO 1 (FATURAS)")
            logger.info("=" * 60)
            
            current_year = datetime.now().year
            start_year = self.config.MODEL_1_START_YEAR
            
            logger.info(f"Período: {start_year} até {current_year}")
            logger.info(f"Total de anos: {current_year - start_year + 1}")
            
            model_1_files = []
            
            for year in range(start_year, current_year + 1):
                logger.info(f"\n--- Processando ano {year} ---")
                
                try:
                    export_url_1 = self.generate_export_model_1(token, year)
                    final_name = f"modelo-1_{year}.csv"  # Extensão correta: CSV
                    files_1 = self.download_and_extract_zip(export_url_1, final_filename=final_name)
                    
                    if files_1:
                        all_extracted_files.extend(files_1)
                        model_1_files.extend(files_1)
                        logger.info(f"✓ Modelo 1 ({year}) salvo como: {final_name}")
                    else:
                        logger.warning(f"⚠ Modelo 1 ({year}) - Sem dados disponíveis, pulando...")
                    
                except Exception as e:
                    logger.error(f"✗ Erro ao processar ano {year}: {e}")
                    logger.info(f"Continuando com próximo ano...")
                
                # Pequeno delay entre downloads para não sobrecarregar o servidor
                if year < current_year:
                    time.sleep(2)
            
            # ===== CONSOLIDAR MODELO 1 =====
            if model_1_files:
                consolidated_file = self.consolidate_model_1_files(model_1_files)
                all_extracted_files.append("modelo-1.csv")
            
            # ===== RESUMO FINAL =====
            logger.info("\n" + "=" * 60)
            logger.info("✓ PROCESSO CONCLUÍDO COM SUCESSO!")
            logger.info("=" * 60)
            logger.info(f"Pasta de destino: {self.config.DOWNLOAD_FOLDER}")
            logger.info(f"Total de arquivos baixados: {len(all_extracted_files)}")
            logger.info("\nArquivos:")
            for file in all_extracted_files:
                logger.info(f"  ✓ {file}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Erro durante execução: {str(e)}", exc_info=True)
            return False
        finally:
            self.close()
    
    def close(self):
        try:
            if self.page and not self.page.is_closed():
                self.page.close()
        except Exception as e:
            logger.debug(f"Erro ao fechar página: {e}")
        
        try:
            if self.context:
                self.context.close()
        except Exception as e:
            logger.debug(f"Erro ao fechar contexto: {e}")
        
        try:
            if self.browser:
                self.browser.close()
        except Exception as e:
            logger.debug(f"Erro ao fechar navegador: {e}")
        
        try:
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            logger.debug(f"Erro ao parar playwright: {e}")
        
        logger.info("Navegador fechado")
