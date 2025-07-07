import os
import json
import time
import io
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from telegram import Bot

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Google API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
gspread_client = gspread.authorize(creds)
drive_service = build('drive', 'v3', credentials=creds)

# Planilha a ser monitorada
spreadsheet = gspread_client.open("FallahTraderBot_Clientes")
sheet = spreadsheet.sheet1

# Nome do arquivo de imagem de teste (ajuste conforme seu Drive)
nome_arquivo = "MATRIZ_ENTRADA_BACK.png"

def pegar_chat_ids():
    registros = sheet.get_all_records()
    chat_ids = []
    for registro in registros:
        chat_id = str(registro.get('Telegram Chat ID')).strip()
        if chat_id and chat_id != '' and chat_id != 'Telegram Chat ID':
            chat_ids.append(chat_id)
    return chat_ids

def buscar_arquivo_drive(nome_arquivo):
    resultados = drive_service.files().list(q=f"name='{nome_arquivo}'", fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])
    if arquivos:
        return arquivos[0]['id']
    else:
        print(f"Arquivo '{nome_arquivo}' não encontrado no Drive.")
        return None

def enviar_imagem_para_clientes(mensagem, arquivo_id):
    request = drive_service.files().get_media(fileId=arquivo_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)

    chat_ids = pegar_chat_ids()
    for chat_id in chat_ids:
        try:
            bot.send_photo(chat_id=chat_id, photo=fh, caption=mensagem)
            print(f"✅ Enviado para {chat_id}")
        except Exception as e:
            print(f"Erro ao enviar para {chat_id}: {e}")

def main():
    while True:
        arquivo_id = buscar_arquivo_drive(nome_arquivo)
        if arquivo_id:
            mensagem = "🚨 ENTRADA DISPONÍVEL:\nFluminense x Flamengo | Back Fluminense | Odd 1,90 | 5' 1T | Brasileirão Série A"
            enviar_imagem_para_clientes(mensagem, arquivo_id)
        else:
            print("Aguardando arquivo aparecer no Drive...")

        time.sleep(30)  # verifica a cada 30 segundos

if __name__ == "__main__":
    main()
