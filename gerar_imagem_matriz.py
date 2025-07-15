import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot
from PIL import Image, ImageDraw

logging.basicConfig(level=logging.INFO)

# 🐞 Debug: exibir IDs das pastas que o script está lendo
logging.info("DEBUG → PASTA_ESCUDOS_ID = %s", os.getenv("PASTA_ESCUDOS_ID"))
logging.info("DEBUG → PASTA_ENTRADA_ID = %s", os.getenv("PASTA_ENTRADA_ID"))

# Carregar credenciais do Google
creds_info = os.getenv("GOOGLE_CREDENTIALS_JSON")
if not creds_info:
    logging.error("Variável GOOGLE_CREDENTIALS_JSON não definida. Finalize antes de prosseguir.")
    exit(1)

creds = service_account.Credentials.from_service_account_info(
    eval(creds_info)
)
drive_service = build('drive', 'v3', credentials=creds)

# IDs das pastas do Drive
PASTA_ESCUDOS_ID = os.getenv("PASTA_ESCUDOS_ID")
PASTA_ENTRADA_ID = os.getenv("PASTA_ENTRADA_ID")
if not PASTA_ESCUDOS_ID or not PASTA_ENTRADA_ID:
    logging.error("Variável de ambiente ausente: PASTA_ESCUDOS_ID ou PASTA_ENTRADA_ID; finalize antes de prosseguir.")
    exit(1)

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    logging.error("Variável de ambiente ausente: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID; finalize antes de prosseguir.")
    exit(1)

bot = Bot(token=BOT_TOKEN)

def baixar_arquivo(folder_id, file_name, dest_path):
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    resp = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = resp.get('files', [])
    if not files:
        logging.error("Arquivo '%s' não encontrado na pasta %s", file_name, folder_id)
        return None
    file_id = files[0]['id']
    drive_service.files().get_media(fileId=file_id).execute()
    request = drive_service.files().get_media(fileId=file_id)
    with open(dest_path, 'wb') as fh:
        fh.write(request.execute())
    logging.info("✔ Arquivo '%s' baixado em '%s'.", file_name, dest_path)
    return dest_path

def gerar_imagem():
    entrada = baixar_arquivo(PASTA_ENTRADA_ID, 'Matriz Entrada Back Exchange.png', 'matrizes_oficiais/entrada.png')
    if not entrada:
        return None

    # exemplo simples: abre a entrada e salva preenchida
    img = Image.open(entrada)
    draw = ImageDraw.Draw(img)
    draw.text((50, 100), "Fluminense vs Flamengo", fill="white")
    destino = 'matrizes_oficiais/matriz_entrada_preenchida.png'
    img.save(destino)
    logging.info("✔ Imagem gerada e salva em '%s'.", destino)
    return destino

def enviar_telegram(caminho):
    if not os.path.exists(caminho):
        logging.error("Arquivo '%s' não encontrado para envio.", caminho)
        return False
    with open(caminho, 'rb') as f:
        bot.send_photo(chat_id=CHAT_ID, photo=f)
    logging.info("✔ Enviado ao Telegram: %s", caminho)
    return True

def main():
    img_path = gerar_imagem()
    if img_path:
        enviar_telegram(img_path)

if __name__ == '__main__':
    main()


