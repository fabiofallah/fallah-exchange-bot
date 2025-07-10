import os
import io
import logging
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2 import service_account

def baixar_arquivo_drive(nome_arquivo, pasta_id, destino):
    try:
        creds_dict = eval(os.environ['GOOGLE_CREDENTIALS_JSON'])
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        service = build('drive', 'v3', credentials=creds)

        # Cria a pasta de destino se não existir
        pasta_destino = os.path.dirname(destino)
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            logging.info(f"📂 Pasta '{pasta_destino}' criada automaticamente.")

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta de ID '{pasta_id}'.")
            return None

        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destino, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logging.info(f"⬇️ Download {int(status.progress() * 100)}% concluído.")

        logging.info(f"✅ Arquivo '{nome_arquivo}' baixado com sucesso em '{destino}'.")
        return destino

    except Exception as e:
        logging.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return None
