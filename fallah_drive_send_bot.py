import os
import json
import io
import gspread
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot

# Configurações iniciais
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_IDS = ['1810082886']  # ou busque da planilha automaticamente se já estiver configurado
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Autenticação no Google Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
gc = gspread.authorize(creds)

def download_file_from_drive(file_name, local_path):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    gauth = GoogleAuth()
    gauth.credentials = creds
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': f"title='{file_name}' and trashed=false"}).GetList()
    if not file_list:
        print(f"Arquivo '{file_name}' não encontrado no Drive.")
        return False
    file_drive = file_list[0]
    file_drive.GetContentFile(local_path)
    print(f"Arquivo '{file_name}' baixado com sucesso.")
    return True

async def send_image():
    file_name = "MATRIZ_ENTRADA_BACK.png"
    local_file = "/tmp/" + file_name

    print("🔄 Procurando arquivo no Drive...")
    if download_file_from_drive(file_name, local_file):
        print("📤 Enviando imagem ao Telegram...")
        with open(local_file, 'rb') as fh:
            for chat_id in CHAT_IDS:
                await bot.send_photo(chat_id=chat_id, photo=fh, caption="📈 ENTRADA AUTOMÁTICA ENVIADA PELO ROBÔ FALLAH ✅")
        print("✅ Imagem enviada para todos os clientes.")
    else:
        print("⚠️ Arquivo não encontrado, não foi possível enviar.")

if __name__ == '__main__':
    asyncio.run(send_image())
