from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import logging

def baixar_arquivo_drive(nome_arquivo, pasta_id, destino):
    try:
        # Credenciais do ambiente Railway
        creds_json = os.environ['GOOGLE_CREDENTIALS_JSON']
        creds_dict = eval(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict)

        service = build('drive', 'v3', credentials=creds)

        # Procurar o arquivo pelo nome na pasta especificada
        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"Arquivo {nome_arquivo} não encontrado na pasta {pasta_id}.")
            return None

        file_id = items[0]['id']

        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destino, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logging.info(f"Download {int(status.progress() * 100)}%.")

        logging.info(f"Arquivo {nome_arquivo} baixado como {destino}.")
        return destino

    except Exception as e:
        logging.error(f"Erro ao baixar arquivo do Drive: {e}")
        return None
