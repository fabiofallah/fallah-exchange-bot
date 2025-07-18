import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from io import BytesIO
import requests  # para fallback URL

# Carrega variáveis
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
CREDS_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
DRIVE_FOLDER_ID = os.environ['PASTA_ENTRADA_ID']

# Autenticação gspread
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(CREDS_JSON), scope)
gc = gspread.authorize(creds)

# Serviço Drive API
drive = build('drive', 'v3', credentials=creds)

bot = Bot(token=TOKEN)

def buscar_entrada():
    sheet = gc.open_by_key(SPREADSHEET_ID).worksheet('Fallah_Clientes_Oficial')
    return sheet.get_all_values()

def puxar_imagem():
    try:
        resp = drive.files().list(q=f"'{DRIVE_FOLDER_ID}' in parents and mimeType contains 'image/'",
                                  orderBy='createdTime desc', pageSize=1).execute()
        file = resp['files'][0]
        dl = drive.files().get_media(fileId=file['id']).execute()
        return BytesIO(dl), file['name']
    except (IndexError, HttpError) as e:
        print("Erro imagem:", e)
        return None, None

def main():
    dados = buscar_entrada()
    img_buffer, name = puxar_imagem()
    if img_buffer:
        bot.send_photo(chat_id=CHAT_ID, photo=img_buffer, caption="✅ Entrada automática")
    else:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Sem imagem encontrada.")
    print("Envio concluído.")

if __name__ == '__main__':
    main()
