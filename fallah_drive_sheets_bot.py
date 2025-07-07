import os
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Configuração do Telegram Bot
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Configuração do Google Sheets e Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abertura da planilha de clientes
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Xj1JCvL8V3WTAB5GxH4gwCTGnSVdGq-sTkHpkVUVDpw/edit#gid=0")
sheet = spreadsheet.sheet1

# Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

def pegar_telegram_id_cliente():
    registros = sheet.get_all_records()
    chat_ids = []
    for registro in registros:
        chat_id = str(registro.get('Telegram Chat ID')).strip()
        if chat_id and chat_id != '':
            chat_ids.append(chat_id)
    return chat_ids

def enviar_mensagem_para_clientes(mensagem, arquivo_id=None):
    chat_ids = pegar_telegram_id_cliente()
    for chat_id in chat_ids:
        if arquivo_id:
            request = drive_service.files().get_media(fileId=arquivo_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.seek(0)
            bot.send_photo(chat_id=chat_id, photo=fh, caption=mensagem)
        else:
            bot.send_message(chat_id=chat_id, text=mensagem)

def buscar_arquivo_drive_por_nome(nome_arquivo):
    resultados = drive_service.files().list(q=f"name='{nome_arquivo}'", fields="files(id, name)").execute()
    arquivos = resultados.get('files', [])
    if arquivos:
        return arquivos[0]['id']
    else:
        return None

def main():
    while True:
        # Exemplo de envio automático (ajuste para checar sinais reais depois)
        mensagem = "🚨 ENTRADA DISPONÍVEL:\nFluminense x Flamengo\nBack Fluminense | Odd: 1,90 | 5' - 1T"
        nome_arquivo = "MATRIZ_ENTRADA_BACK.png"
        arquivo_id = buscar_arquivo_drive_por_nome(nome_arquivo)
        enviar_mensagem_para_clientes(mensagem, arquivo_id)
        print("Enviado com sucesso para os clientes da planilha.")

        time.sleep(3600)  # Executa a cada 1 hora (ajuste conforme necessário)

if __name__ == "__main__":
    main()
