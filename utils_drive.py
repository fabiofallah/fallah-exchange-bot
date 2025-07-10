# utils_drive.py corrigido para pegar automaticamente os IDs corretos das variáveis de ambiente

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import logging

def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino):
    try:
        creds_json = os.environ['GOOGLE_CREDENTIALS_JSON']
        creds_dict = eval(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        service = build('drive', 'v3', credentials=creds)

        # Mapeamento dinâmico usando variáveis de ambiente
        tipo_operacao_upper = tipo_operacao.upper()
        pasta_id = os.getenv(f'PASTA_{tipo_operacao_upper}_ID')

        if not pasta_id:
            logging.error(f"❌ Tipo de operação '{tipo_operacao}' não possui variável de ambiente configurada.")
            return None

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta do tipo '{tipo_operacao}'.")
            return None

        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destino, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            if status:
                logging.info(f"⬇️ Download {int(status.progress() * 100)}% concluído para '{nome_arquivo}'.")

        logging.info(f"✅ Arquivo '{nome_arquivo}' baixado com sucesso para '{destino}'.")
        return destino

    except Exception as e:
        logging.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return None
