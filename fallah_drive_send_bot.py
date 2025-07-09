import os
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from telegram import Bot
import io
from PIL import Image, ImageDraw, ImageFont

# Configurações iniciais
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
SCOPES = ['https://www.googleapis.com/auth/drive']

# Credenciais do Google Drive
creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# IDs fixos das pastas (atualizados)
PASTA_ENTRADA_ID = '1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz'

# Nome do arquivo de entrada
NOME_ARQUIVO_ENTRADA = 'Matriz Entrada Back Exchange.png'

# Função para baixar arquivo do Drive
def baixar_arquivo_drive(file_name, folder_id, local_file_name):
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        logging.error(f"Arquivo {file_name} não encontrado na pasta {folder_id}.")
        return None

    file_id = items[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        logging.info(f"Download {int(status.progress() * 100)}%.")

    fh.seek(0)
    with open(local_file_name, 'wb') as f:
        f.write(fh.read())

    logging.info(f"Arquivo {local_file_name} baixado com sucesso.")
    return local_file_name

# Função para preencher a matriz automaticamente
def preencher_matriz():
    matriz_path = baixar_arquivo_drive(NOME_ARQUIVO_ENTRADA, PASTA_ENTRADA_ID, 'matriz_entrada.png')
    if matriz_path is None:
        return

    # Abrir imagem e preparar para edição
    image = Image.open(matriz_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Dados fictícios de teste (ajuste conforme desejar)
    draw.text((60, 430), "MetLife Stadium", fill="black", font=font)
    draw.text((60, 470), "Super Mundial FIFA", fill="black", font=font)
    draw.text((60, 510), "1.90", fill="black", font=font)
    draw.text((60, 550), "R$ 100", fill="black", font=font)
    draw.text((60, 590), "Back PSG", fill="black", font=font)
    draw.text((60, 630), "450K", fill="black", font=font)
    draw.text((60, 670), "16:00", fill="black", font=font)
    draw.text((60, 710), "-", fill="black", font=font)

    # Salvar a imagem preenchida
    output_image_path = 'matriz_entrada_preenchida.png'
    image.save(output_image_path)
    logging.info("Imagem da matriz preenchida gerada com sucesso.")

    # Enviar via Telegram
    bot = Bot(token=BOT_TOKEN)
    with open(output_image_path, 'rb') as photo:
        bot.send_photo(chat_id=CHAT_ID, photo=photo)

    logging.info("Imagem enviada ao Telegram com sucesso.")

# Execução
def main():
    logging.info("Iniciando envio automático da matriz de ENTRADA...")
    preencher_matriz()

if __name__ == '__main__':
    main()

