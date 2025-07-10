import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from telegram import Bot
import asyncio
import io

logging.basicConfig(level=logging.INFO)

async def enviar_foto_telegram(bot, chat_id, image_path):
    with open(image_path, 'rb') as img:
        await bot.send_photo(chat_id=chat_id, photo=img)
    logging.info(f"✅ Imagem '{image_path}' enviada com sucesso ao Telegram.")

async def main():
    try:
        # Configurações
        TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logging.error("❌ TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurados no Railway.")
            return

        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        # Baixar arquivo do Drive
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if creds_json is None:
            logging.error("❌ Credenciais do Google não encontradas nas variáveis de ambiente.")
            return

        creds = Credentials.from_service_account_info(eval(creds_json))
        service = build('drive', 'v3', credentials=creds)

        pasta_id = os.environ.get('PASTA_ENTRADA_ID')
        if pasta_id is None:
            logging.error("❌ ID da pasta de entrada não configurado no Railway.")
            return

        nome_arquivo = 'Matriz Entrada Back Exchange.png'
        destino = 'matrizes_oficiais/Matriz Entrada Back Exchange.png'

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo '{nome_arquivo}' não encontrado no Drive.")
            return

        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)

        os.makedirs(os.path.dirname(destino), exist_ok=True)

        with io.FileIO(destino, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logging.info(f"📥 Download {int(status.progress() * 100)}% concluído.")
        logging.info(f"✅ Arquivo '{nome_arquivo}' baixado e salvo em '{destino}'.")

        # Enviar ao Telegram de forma assíncrona
        await enviar_foto_telegram(bot, TELEGRAM_CHAT_ID, destino)

    except Exception as e:
        logging.error(f"❌ Erro no processo: {e}")

if __name__ == '__main__':
    asyncio.run(main())
