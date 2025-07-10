# Substitua o conteúdo de 'fallah_drive_send_bot.py' por este script corrigido

import os
import logging
from utils_drive import baixar_arquivo_drive
from telegram import Bot

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

tipo_operacao = 'ENTRADA'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'

# Diretório onde a matriz será salva
pasta_matrizes = '/app/matrizes_oficiais'
os.makedirs(pasta_matrizes, exist_ok=True)

# Caminho completo do arquivo após download
caminho_matriz = os.path.join(pasta_matrizes, matriz_nome_drive)

# Download se não existir localmente
if not os.path.exists(caminho_matriz):
    logger.warning(f"Arquivo '{matriz_nome_drive}' não encontrado em '{pasta_matrizes}'. Tentando baixar do Drive...")
    sucesso = baixar_arquivo_drive(matriz_nome_drive, tipo_operacao, caminho_matriz)
    if not sucesso:
        logger.error(f"Falha ao baixar '{matriz_nome_drive}' do Drive.")
        exit(1)
else:
    logger.info(f"Arquivo '{matriz_nome_drive}' encontrado localmente em '{pasta_matrizes}'.")

# Enviar ao Telegram
try:
    bot = Bot(token=TOKEN)
    with open(caminho_matriz, 'rb') as imagem:
        bot.send_photo(chat_id=CHAT_ID, photo=imagem)
    logger.info(f"Imagem '{matriz_nome_drive}' enviada com sucesso ao Telegram.")
except Exception as e:
    logger.error(f"Erro ao enviar imagem ao Telegram: {e}")
