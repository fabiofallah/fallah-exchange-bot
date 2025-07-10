import os
import logging
from utils_drive import baixar_arquivo_drive
from telegram import Bot

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do bot Telegram
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
bot = Bot(token=bot_token)

# Caminho e nome do arquivo a ser baixado
tipo_operacao = 'ENTRADA'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'
pasta_matrizes = '/app/matrizes_oficiais'
caminho_matriz = os.path.join(pasta_matrizes, matriz_nome_drive)

# Cria a pasta caso não exista
os.makedirs(pasta_matrizes, exist_ok=True)

# Se não existir localmente, baixa do Drive
if not os.path.isfile(caminho_matriz):
    logger.warning(f"Arquivo '{matriz_nome_drive}' não encontrado localmente. Tentando baixar do Drive...")
    download = baixar_arquivo_drive(matriz_nome_drive, tipo_operacao, caminho_matriz)
    if download:
        logger.info(f"Arquivo '{matriz_nome_drive}' baixado e salvo em '{caminho_matriz}'.")
    else:
        logger.error(f"Falha ao baixar o arquivo '{matriz_nome_drive}' do Drive.")
        exit(1)
else:
    logger.info(f"Arquivo '{matriz_nome_drive}' encontrado localmente.")

# Verificação de arquivo para envio correto
if os.path.isfile(caminho_matriz):
    try:
        with open(caminho_matriz, 'rb') as img:
            bot.send_photo(chat_id=chat_id, photo=img)
        logger.info(f"✅ Imagem '{matriz_nome_drive}' enviada com sucesso ao Telegram.")
    except Exception as e:
        logger.error(f"Erro ao enviar imagem ao Telegram: {e}")
else:
    logger.error(f"O caminho '{caminho_matriz}' não é um arquivo válido para envio.")

