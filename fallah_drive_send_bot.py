import os
import logging
import asyncio
from telegram import Bot
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import io

# Configuração de logs
logging.basicConfig(level=logging.INFO)

# ✅ Função para baixar do Google Drive
def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino):
    try:
        logging.info("🔹 Iniciando download da matriz do Drive...")

        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        creds = Credentials.from_service_account_info(eval(creds_json))
        service = build('drive', 'v3', credentials=creds)

        pasta_id = os.environ.get(f'PASTA_{tipo_operacao.upper()}_ID')
        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo {nome_arquivo} não encontrado no Drive.")
            return False

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
        return destino

    except Exception as e:
        logging.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return False

# ✅ Função principal assíncrona para envio
async def main():
    try:
        TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        # Baixar a matriz
        destino = 'matrizes_oficiais/Matriz Entrada Back Exchange.png'
        baixar_arquivo_drive('Matriz Entrada Back Exchange.png', 'ENTRADA', destino)

        # Gerar a imagem automaticamente com dados
        logging.info("⚡ Gerando imagem com dados e escudo...")
        import gerar_imagem_matriz  # importa e executa automaticamente o script de geração
        logging.info("✅ Imagem gerada, enviando ao Telegram...")

        img_path = 'matrizes_oficiais/matriz_entrada_preenchida.png'

        # Confirma se existe antes do envio
        if not os.path.exists(img_path):
            logging.error(f"❌ Arquivo '{img_path}' não encontrado para envio.")
            return

        # Envio ao Telegram
        with open(img_path, 'rb') as img:
            response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)
            logging.info(f"✅ Imagem enviada com sucesso ao Telegram. Resposta: {response}")

    except Exception as e:
        logging.error(f"❌ Erro no envio ao Telegram: {e}")

if __name__ == '__main__':
    asyncio.run(main())
