import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import io

def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino):
    try:
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if creds_json is None:
            logging.error("❌ Credenciais do Google não encontradas nas variáveis de ambiente.")
            return False

        creds = Credentials.from_service_account_info(eval(creds_json))
        service = build('drive', 'v3', credentials=creds)

        pasta_id = os.environ.get(f'PASTA_{tipo_operacao.upper()}_ID')
        if pasta_id is None:
            logging.error(f"❌ ID da pasta para {tipo_operacao} não encontrada nas variáveis de ambiente.")
            return False

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo {nome_arquivo} não encontrado na pasta do Drive.")
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

        if os.path.isfile(destino):
            return destino
        else:
            logging.error(f"❌ O caminho '{destino}' não é um arquivo válido para envio.")
            return False

    except Exception as e:
        logging.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return False
