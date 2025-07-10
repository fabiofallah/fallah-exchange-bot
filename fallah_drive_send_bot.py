import os
import logging
from telegram import Bot
from utils_drive import baixar_arquivo_drive

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
pasta_matriz = '/app/matrizes_oficiais/'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'
tipo_operacao = 'ENTRADA'  # ajustável futuramente se desejar

# Caminho completo onde será salvo
caminho_matriz = os.path.join(pasta_matriz, matriz_nome_drive)

# Verifica e baixa caso necessário
if not os.path.exists(caminho_matriz):
    logger.warning(f"⚠️ Arquivo '{matriz_nome_drive}' não encontrado em '{pasta_matriz}'. Tentando baixar do Drive...")
    download = baixar_arquivo_drive(matriz_nome_drive, tipo_operacao, caminho_matriz)
    if download:
        logger.info(f"✅ Arquivo '{matriz_nome_drive}' baixado e salvo em '{caminho_matriz}'.")
    else:
        logger.error(f"❌ Falha ao baixar o arquivo '{matriz_nome_drive}' do Drive.")
        exit(1)
else:
    logger.info(f"✅ Arquivo '{matriz_nome_drive}' encontrado localmente em '{pasta_matriz}'.")

# Envio ao Telegram
try:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open(caminho_matriz, 'rb') as photo:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption="📊 MATRIZ ENVIADA AUTOMATICAMENTE")
    logger.info(f"✅ Imagem '{matriz_nome_drive}' enviada ao Telegram com sucesso.")
except Exception as e:
    logger.error(f"❌ Erro ao enviar imagem ao Telegram: {e}")
