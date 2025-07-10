import os
import logging
from utils_drive import baixar_arquivo_drive

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome do arquivo a ser buscado
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'
tipo_operacao = 'ENTRADA'  # ajuste dinamicamente em seu fluxo quando precisar buscar RESULTADO, CONEXAO, etc.

# Caminho local onde a matriz será salva
pasta_matriz = '/app/matrizes_oficiais/'
caminho_matriz = os.path.join(pasta_matriz, matriz_nome_drive)

# Verifica se o arquivo existe localmente, se não existir busca no Drive automaticamente
if not os.path.exists(caminho_matriz):
    logger.warning(f"⚠️ Arquivo '{matriz_nome_drive}' não encontrado em '{pasta_matriz}'. Tentando baixar do Drive...")
    download = baixar_arquivo_drive(matriz_nome_drive, tipo_operacao, caminho_matriz)
    if download:
        logger.info(f"✅ Arquivo '{matriz_nome_drive}' baixado do Drive e salvo em '{caminho_matriz}'.")
    else:
        logger.error(f"❌ Falha ao baixar o arquivo '{matriz_nome_drive}' do Drive.")
        exit(1)
else:
    logger.info(f"✅ Arquivo '{matriz_nome_drive}' encontrado localmente em '{pasta_matriz}'.")

# Continuação do seu processo normal:
# import cv2
# matriz = cv2.imread(caminho_matriz)
# ...
