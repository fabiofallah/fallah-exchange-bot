import os
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from telegram import Bot

# === CONFIGURAÇÕES ===
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = 'SEU_CHAT_ID_AQUI'  # substitua pelo seu se não estiver usando planilha de clientes

# === AUTENTICAÇÃO GOOGLE DRIVE ===
creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
if creds_json is None:
    raise Exception("Variável de ambiente GOOGLE_CREDENTIALS_JSON não encontrada")

credentials_info = json.loads(creds_json)
creds = service_account.Credentials.from_service_account_info(credentials_info, scopes=['https://www.googleapis.com/auth/drive'])

service = build('drive', 'v3', credentials=creds)

# === BUSCA DO ARQUIVO ESPECÍFICO NA PASTA ENTRADA ===
# PEGUE O ID DA PASTA ENTRADA E SUBSTITUA AQUI:
PASTA_ENTRADA_ID = 'COLE_AQUI_O_ID_DA_PASTA_ENTRADA'

query = f"'{PASTA_ENTRADA_ID}' in parents and name = 'Matriz Entrada Back Exchange.png' and trashed = false"
results = service.files().list(q=query, fields="files(id, name)").execute()
items = results.get('files', [])

if not items:
    print("Arquivo não encontrado.")
else:
    file_id = items[0]['id']
    file_name = items[0]['name']

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)

    # === ENVIO PARA O TELEGRAM ===
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_photo(chat_id=CHAT_ID, photo=fh)

    print(f"{file_name} enviado com sucesso para o Telegram.")
