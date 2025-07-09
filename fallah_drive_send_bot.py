import os
import json
import logging
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do Bot Telegram
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Credenciais via variável de ambiente
creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
credentials = service_account.Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/drive"])

# IDs das pastas do Drive
PASTAS = {
    'ENTRADA': '1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz',
    'CORRESPONDENCIA': '1eIj28u_wyuS0szW4a2ux5O_zD4qzrafk',
    'RESULTADO': '1dqWvl6J-qhTuYAQ15gc9atMduOXuzQB_',
    'CONEXAO': '1kpTe1zLqE7DV7Inxsin171SD5_QIh_KP'
}

async def enviar_imagem():
    try:
        logger.info("Iniciando envio da matriz de ENTRADA...")

        drive_service = build('drive', 'v3', credentials=credentials)
        query = f"'{PASTAS['ENTRADA']}' in parents and mimeType contains 'image/' and trashed = false"

        results = drive_service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            logger.info("Nenhuma imagem encontrada na pasta de ENTRADA.")
            return

        file_id = files[0]['id']
        file_name = files[0]['name']

        logger.info(f"Baixando {file_name}...")

        request = drive_service.files().get_media(fileId=file_id)
        file_bytes = request.execute()

        await bot.send_photo(chat_id=CHAT_ID, photo=file_bytes)
        logger.info(f"Imagem {file_name} enviada com sucesso ao Telegram.")

    except Exception as e:
        logger.error(f"Erro ao enviar imagem: {e}")

if __name__ == '__main__':
    asyncio.run(enviar_imagem())

