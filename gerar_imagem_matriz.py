import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import telegram
import logging

# Configurações básicas
logging.basicConfig(level=logging.INFO)
ESCUDOS_FOLDER_ID = os.getenv("PASTA_ESCUDOS_ID")
MATRIZ_FOLDER = "matrizes_oficiais"
MATRIZ_NOME = "Matriz Entrada Back Exchange.png"
MATRIZ_SAIDA = "matriz_entrada_preenchida.png"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Função para baixar arquivo do Google Drive
def baixar_arquivo(service, file_id, nome_destino):
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(nome_destino, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()

# Função principal
def main():
    from google.oauth2 import service_account
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    creds = service_account.Credentials.from_service_account_info(eval(creds_json))
    service = build('drive', 'v3', credentials=creds)

    logging.info("🔵 Iniciando download da matriz do Drive...")
    results = service.files().list(q=f"name='{MATRIZ_NOME}'", fields="files(id)").execute()
    files = results.get('files', [])

    if not files:
        logging.error("❌ Matriz não encontrada no Drive.")
        return

    matriz_id = files[0]['id']
    os.makedirs(MATRIZ_FOLDER, exist_ok=True)
    caminho_matriz = os.path.join(MATRIZ_FOLDER, MATRIZ_NOME)
    baixar_arquivo(service, matriz_id, caminho_matriz)
    logging.info(f"✅ Arquivo '{MATRIZ_NOME}' baixado e salvo em '{caminho_matriz}'.")

    # Carrega matriz
    imagem = cv2.imread(caminho_matriz)

    # Aqui vai a edição real da imagem...
    cv2.putText(imagem, "BACK", (95, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Salvando imagem final com nome fixo
    caminho_saida = os.path.join(MATRIZ_FOLDER, MATRIZ_SAIDA)
    sucesso = cv2.imwrite(caminho_saida, imagem)

    if not sucesso or not os.path.exists(caminho_saida):
        logging.error(f"❌ Falha ao salvar a imagem final em '{caminho_saida}'.")
        return

    logging.info("✅ Imagem gerada, enviando ao Telegram...")

    bot = telegram.Bot(token=TOKEN)
    with open(caminho_saida, 'rb') as photo:
        bot.send_photo(chat_id=CHAT_ID, photo=photo)

if __name__ == "__main__":
    main()
