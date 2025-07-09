import os
import logging
import telegram
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

# Configuração
TELEGRAM_BOT_TOKEN = 'INSIRA_SEU_TOKEN_AQUI'
TELEGRAM_CHAT_ID = 'INSIRA_SEU_CHAT_ID_AQUI'

FOLDER_IDS = {
    "ENTRADA": "ID_DA_PASTA_ENTRADA",
    "CORRESPONDÊNCIA": "ID_DA_PASTA_CORRESPONDENCIA",
    "RESULTADO": "ID_DA_PASTA_RESULTADO",
}

# Nome dos arquivos específicos para teste controlado
ARQUIVOS_PERMITIDOS = {
    "ENTRADA": "Matriz Entrada Back Exchange.png",
    "CORRESPONDÊNCIA": "Matriz Correspondência Back Exchange.png",
    "RESULTADO": "Matriz Resultado Back Exchange.png",
}

# Inicializa bot Telegram
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# Inicializa Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Configuração de log
logging.basicConfig(level=logging.INFO)

def check_and_send(folder_name):
    folder_id = FOLDER_IDS[folder_name]
    target_filename = ARQUIVOS_PERMITIDOS[folder_name]

    query = f"'{folder_id}' in parents and name = '{target_filename}' and trashed = false"
    results = drive_service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        logging.info(f"Sem {target_filename} em {folder_name}.")
    else:
        item = items[0]
        request = drive_service.files().get_media(fileId=item['id'])
        filename = item['name']
        filepath = f'/tmp/{filename}'

        with open(filepath, 'wb') as f:
            downloader = drive_service.files().get_media(fileId=item['id'])
            done = False
            while done is False:
                status, done = downloader.next_chunk()

        with open(filepath, 'rb') as photo:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
            logging.info(f"Imagem {filename} enviada ao Telegram sem legenda.")

        # Após enviar, mover para lixeira
        drive_service.files().update(fileId=item['id'], body={'trashed': True}).execute()
        logging.info(f"{filename} movido para a lixeira após envio.")

def main():
    while True:
        for pasta in ["ENTRADA", "CORRESPONDÊNCIA", "RESULTADO"]:
            check_and_send(pasta)
            time.sleep(2)
        time.sleep(10)

if __name__ == '__main__':
    main()
