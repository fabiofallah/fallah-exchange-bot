import os
import json
import logging
import asyncio
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from telegram import Bot

# Configurações
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_INFO = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PASTA_ENTRADA_ID = '1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz'  # Pasta ENTRADA
ARQUIVO_ENTRADA_NOME = 'Matriz Entrada Back Exchange.png'

# Função para baixar arquivo do Google Drive
def baixar_arquivo_drive(nome_arquivo, id_pasta, nome_saida):
    creds = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    query = f"name='{nome_arquivo}' and '{id_pasta}' in parents and trashed=false"
    results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado na pasta do Drive.")

    file_id = items[0]['id']
    request = service.files().get_media(fileId=file_id)

    with open(nome_saida, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logging.info(f"Download {int(status.progress() * 100)}%.")

    logging.info(f"Arquivo {nome_saida} baixado com sucesso.")
    return nome_saida

def preencher_matriz(imagem_path):
    img = Image.open(imagem_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 48)

    draw.text((50, 550), "MetLife Stadium", fill="black", font=font)
    draw.text((50, 650), "FIFA Club World Cup", fill="black", font=font)
    draw.text((50, 750), "2.44", fill="black", font=font)
    draw.text((50, 850), "R$ 100", fill="black", font=font)
    draw.text((50, 950), "Match Odds", fill="black", font=font)
    draw.text((50, 1050), "450K", fill="black", font=font)
    draw.text((50, 1150), "16:00", fill="black", font=font)
    draw.text((50, 1250), "--", fill="black", font=font)

    imagem_saida = "matriz_preenchida.png"
    img.save(imagem_saida)
    logging.info("Imagem da matriz preenchida gerada com sucesso.")
    return imagem_saida

async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Iniciando envio automático da matriz de ENTRADA...")
    
    matriz_path = baixar_arquivo_drive(ARQUIVO_ENTRADA_NOME, PASTA_ENTRADA_ID, 'matriz_entrada.png')
    matriz_preenchida_path = preencher_matriz(matriz_path)
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open(matriz_preenchida_path, 'rb') as photo:
        await bot.send_photo(chat_id=CHAT_ID, photo=photo)
    logging.info("Imagem enviada ao Telegram com sucesso.")

if __name__ == "__main__":
    asyncio.run(main())

