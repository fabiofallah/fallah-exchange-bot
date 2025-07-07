import os
import json
import io
import gspread
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot

# Configurações iniciais
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_IDS = ['1810082886']
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Autenticação no Google Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
gc = gspread.authorize(creds)

def list_png_files_from_drive():
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    gauth = GoogleAuth()
    gauth.credentials = creds
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "mimeType='image/png' and trashed=false"}).GetList()
    return file_list

def download_file_from_drive(file_drive, local_path):
    file_drive.GetContentFile(local_path)
    print(f"Arquivo '{file_drive['title']}' baixado com sucesso.")

async def send_all_images():
    print("🔄 Buscando arquivos PNG no Drive...")
    file_list = list_png_files_from_drive()
    if not file_list:
        print("⚠️ Nenhum arquivo PNG encontrado no Drive.")
        return

    for file_drive in file_list:
        local_file = "/tmp/" + file_drive['title']
        download_file_from_drive(file_drive, local_file)

        print(f"📤 Enviando '{file_drive['title']}' ao Telegram como DOCUMENTO...")
        for chat_id in CHAT_IDS:
            with open(local_file, 'rb') as fh:
                await bot.send_document(chat_id=chat_id, document=fh, caption="📈 ENVIO AUTOMÁTICO PELO ROBÔ FALLAH ✅")
        print(f"✅ '{file_drive['title']}' enviada para todos os clientes.\n")

if __name__ == '__main__':
    asyncio.run(send_all_images())
