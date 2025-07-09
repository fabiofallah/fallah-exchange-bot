import os
import json
import logging
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot

# Logging para Railway
logging.basicConfig(level=logging.INFO)

# Credenciais do Google
creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
creds_dict = json.loads(creds_json)
creds = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

# Bot Token e inicialização
telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = Bot(token=telegram_token)

# Chat ID do cliente
CHAT_ID = "1810082886"

# IDs das pastas no Google Drive
FOLDER_IDS = {
    "CONEXAO": "1kpTe1zLqE7DV7Inxsin171SD5_QIh_KP",
    "ENTRADA": "1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz",
    "CORRESPONDENCIA": "1eIj28u_wyuS0szW4a2ux5O_zD4qzrafk",
    "RESULTADO": "1dqWvl6J-qhTuYAQ15gc9atMduOXuzQB_"
}

# Serviço do Drive
service = build('drive', 'v3', credentials=creds)

# Tipo de teste (trocar se desejar)
TEST_TYPE = "ENTRADA"  # "CONEXAO", "ENTRADA", "CORRESPONDENCIA", "RESULTADO"

def get_latest_file(folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        orderBy="createdTime desc",
        pageSize=1,
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    if not files:
        return None, None
    return files[0]['id'], files[0]['name']

async def download_and_send_file(folder_type):
    folder_id = FOLDER_IDS[folder_type]
    file_id, file_name = get_latest_file(folder_id)

    if file_id and file_name:
        logging.info(f"Baixando arquivo '{file_name}' da pasta {folder_type}...")
        request = service.files().get_media(fileId=file_id)
        with open(file_name, 'wb') as f:
            downloader = request
            downloader.execute()
            f.write(request.execute())

        with open(file_name, 'rb') as photo:
            await bot.send_photo(chat_id=CHAT_ID, photo=photo)
        logging.info(f"✅ Arquivo '{file_name}' enviado com sucesso ao Telegram.")
    else:
        logging.info(f"Nenhum arquivo encontrado na pasta {folder_type}.")

async def main():
    await download_and_send_file(TEST_TYPE)

if __name__ == '__main__':
    asyncio.run(main())
