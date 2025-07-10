import os
import logging
from utils_drive import baixar_arquivo_drive

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho da pasta onde a matriz deve estar
pasta_matriz = '/app/matrizes_oficiais/'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'

# Monta o caminho completo
caminho_matriz = os.path.join(pasta_matriz, matriz_nome_drive)

# Verifica se o arquivo existe localmente, se não existir baixa do Drive
if not os.path.exists(caminho_matriz):
    logger.warning(f"⚠️ Arquivo '{matriz_nome_drive}' não encontrado localmente em '{pasta_matriz}', tentando baixar do Drive...")
    download = baixar_arquivo_drive(matriz_nome_drive, 'PASTA_ID_DRIVE_ENTRADAS', caminho_matriz)
    if download:
        logger.info(f"✅ Arquivo '{matriz_nome_drive}' baixado do Drive com sucesso.")
    else:
        logger.error(f"❌ Falha ao baixar o arquivo '{matriz_nome_drive}' do Drive.")
        exit(1)
else:
    logger.info(f"✅ Arquivo '{matriz_nome_drive}' encontrado localmente em '{pasta_matriz}'.")

# Aqui segue o seu processo normal
# import cv2
# matriz = cv2.imread(caminho_matriz)
# ...
