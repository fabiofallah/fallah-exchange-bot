# ========================
# FALLAH EXCHANGE BOT AJUSTADO
# Busca automática de imagens nas pastas (ENTRADA, RESULTADO, CORRESPONDENCIA, CONEXAO) do Google Drive
# Busca escudos automaticamente nas pastas de escudos
# Script para substituir o atual utils_drive.py
# ========================

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

        # Dicionário para mapear tipo de operação para o nome da pasta no Drive
        pasta_drive_map = {
            "ENTRADA": 'ID_PASTA_ENTRADA',
            "RESULTADO": 'ID_PASTA_RESULTADO',
            "CORRESPONDENCIA": 'ID_PASTA_CORRESPONDENCIA',
            "CONEXAO": 'ID_PASTA_CONEXAO',
            "AFRICA": 'ID_PASTA_AFRICA',
            "AMERICA": 'ID_PASTA_AMERICA',
            "ASIA": 'ID_PASTA_ASIA',
            "EUROPA": 'ID_PASTA_EUROPA',
            "BANDEIRAS": 'ID_PASTA_BANDEIRAS'
        }

        pasta_id = pasta_drive_map.get(tipo_operacao.upper())

        if not pasta_id:
            logging.error(f"❌ Tipo de operação '{tipo_operacao}' não encontrado no mapeamento.")
            return None

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta de {tipo_operacao}.")
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

        logging.info(f"✅ Arquivo '{nome_arquivo}' baixado para {destino}.")
        return destino

    except Exception as e:
        logging.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return None
