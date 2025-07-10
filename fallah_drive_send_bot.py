import os
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho da pasta onde a matriz deve estar
pasta_matriz = '/app/matrizes_oficiais/'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'

# Monta o caminho completo
caminho_matriz = os.path.join(pasta_matriz, matriz_nome_drive)

# Verifica se o arquivo existe e loga corretamente
if os.path.exists(caminho_matriz):
    logger.info(f"✅ Arquivo '{matriz_nome_drive}' encontrado na pasta {pasta_matriz}.")
else:
    logger.error(f"❌ Arquivo '{matriz_nome_drive}' não encontrado na pasta {pasta_matriz}.")

# Continuação do seu processo normal...
# Aqui você pode carregar e processar a matriz normalmente
# import cv2
# matriz = cv2.imread(caminho_matriz)
# ...
