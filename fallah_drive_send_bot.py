import os
import logging
import subprocess
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import io

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino):
    try:
        logging.info("📥 Iniciando download da matriz do Drive...")
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if creds_json is None:
            logging.error("Credenciais do Google não encontradas nas variáveis de ambiente.")
            return False

        creds = Credentials.from_service_account_info(eval(creds_json))
        service = build('drive', 'v3', credentials=creds)

        pasta_id = os.environ.get(f'PASTA_{tipo_operacao.upper()}_ID')
        if pasta_id is None:
            logging.error(f"ID da pasta para {tipo_operacao} não encontrada nas variáveis de ambiente.")
            return False

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"Arquivo {nome_arquivo} não encontrado na pasta do Drive.")
            return False

        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)

        if not os.path.exists(os.path.dirname(destino)):
            os.makedirs(os.path.dirname(destino))

        with io.FileIO(destino, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logging.info(f"⬇️ Download {int(status.progress() * 100)}% concluído.")

        logging.info(f"✅ Arquivo '{nome_arquivo}' baixado e salvo em '{destino}'.")
        return destino if os.path.isfile(destino) else False

    except Exception as e:
        logging.error(f"Erro ao baixar arquivo do Drive: {e}")
        return False

def main():
    nome_arquivo_drive = "Matriz Entrada Back Exchange.png"
    tipo_operacao = "entrada"
    destino_local = "matrizes_oficiais/Matriz Entrada Back Exchange.png"

    arquivo_baixado = baixar_arquivo_drive(nome_arquivo_drive, tipo_operacao, destino_local)
    if not arquivo_baixado:
        logging.error("❌ Falha ao baixar a matriz do Drive, encerrando processo.")
        return

    try:
        logging.info("⚡ Gerando imagem com dados e escudo...")
        subprocess.run(['python', 'gerar_imagem_matriz.py'], check=True)
        logging.info("✅ Imagem gerada, enviando ao Telegram...")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao gerar imagem matriz: {e}")
        return

    from telegram import Bot

    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        logging.error("TOKEN ou CHAT_ID do Telegram não configurados.")
        return

    bot = Bot(token=bot_token)

    try:
        with open("matrizes_oficiais/matriz_entrada_preenchida.png", 'rb') as img:
            bot.send_photo(chat_id=chat_id, photo=img)
        logging.info("✅ Imagem enviada com sucesso ao Telegram.")
    except Exception as e:
        logging.error(f"Erro ao enviar a imagem ao Telegram: {e}")

if __name__ == "__main__":
    main()
