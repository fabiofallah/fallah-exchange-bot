import os
import logging
from utils_drive import baixar_arquivo_drive

# Configuração de logging clara e limpa
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome do arquivo a ser buscado no Drive
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'

# Pega o ID da pasta de entrada a partir da variável de ambiente
pasta_id = os.environ.get('PASTA_ENTRADA_ID')

# Cria a pasta local caso não exista
pasta_local = '/app/matrizes_oficiais'
os.makedirs(pasta_local, exist_ok=True)

# Caminho completo local
caminho_local = os.path.join(pasta_local, matriz_nome_drive)

# Verifica se o arquivo já existe localmente
if not os.path.exists(caminho_local):
    logger.info(f'Arquivo "{matriz_nome_drive}" não encontrado localmente, tentando baixar do Drive...')
    arquivo_baixado = baixar_arquivo_drive(matriz_nome_drive, pasta_id, caminho_local)
    if arquivo_baixado:
        logger.info(f'✅ Arquivo "{matriz_nome_drive}" baixado com sucesso e salvo em "{caminho_local}".')
    else:
        logger.error(f'❌ Falha ao baixar "{matriz_nome_drive}" do Drive. Verifique se o nome está idêntico no Drive.')
        exit(1)
else:
    logger.info(f'✅ Arquivo "{matriz_nome_drive}" já existe em "{caminho_local}".')

# A partir daqui, prossiga seu processamento normalmente
# import cv2
# matriz = cv2.imread(caminho_local)
# ...
