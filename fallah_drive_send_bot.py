# Envie este script em **fallah_drive_send_bot.py**, substituindo o conteúdo atual
# para testar imediatamente sem mexer em outros arquivos.

import os
import logging
from utils_drive import baixar_arquivo_drive
from telegram import Bot

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Configurações de nome e pasta
pasta_matriz = '/app/matrizes_oficiais/'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'
caminho_matriz = os.path.join(pasta_matriz, matriz_nome_drive)

# Verifica e baixa do Drive se não existir
if not os.path.exists(caminho_matriz):
    logger.warning(f"⚠️ Arquivo '{matriz_nome_drive}' não encontrado em '{pasta_matriz}'. Tentando baixar do Drive...")
    download = baixar_arquivo_drive(matriz_nome_drive, 'ENTRADA', caminho_matriz)
    if download:
        logger.info(f"✅ Arquivo '{matriz_nome_drive}' baixado e salvo em '{caminho_matriz}'.")
    else:
        logger.error(f"❌ Falha ao baixar o arquivo '{matriz_nome_drive}' do Drive.")
        exit(1)
else:
    logger.info(f"✅ Arquivo '{matriz_nome_drive}' encontrado localmente em '{pasta_matriz}'.")

# Envio ao Telegram
try:
    bot = Bot(token=TOKEN)
    with open(caminho_matriz, 'rb') as arquivo:
        bot.send_document(chat_id=CHAT_ID, document=arquivo, caption='✅ MATRIZ ENVIADA COM SUCESSO')
    logger.info(f"✅ Imagem '{matriz_nome_drive}' enviada ao Telegram com sucesso.")
except Exception as e:
    logger.error(f"❌ Erro ao enviar imagem ao Telegram: {e}")
