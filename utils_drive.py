import os
import io
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino_pasta='/app/matrizes_oficiais/'):
    try:
        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Cria a pasta caso não exista
        if not os.path.exists(destino_pasta):
            os.makedirs(destino_pasta)
            logger.info(f"📁 Pasta '{destino_pasta}' criada automaticamente.")

        # Credenciais
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        creds_dict = eval(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict)

        service = build('drive', 'v3', credentials=creds)

        # Mapeamento de pastas
        pasta_drive_map = {
            'ENTRADA': os.environ.get('PASTA_ENTRADA_ID'),
            'RESULTADO': os.environ.get('PASTA_RESULTADO_ID'),
            'CORRESPONDENCIA': os.environ.get('PASTA_CORRESPONDENCIA_ID'),
            'CONECAO': os.environ.get('PASTA_CONEXAO_ID'),
            'AFRICA': os.environ.get('PASTA_AFRICA_ID'),
            'AMERICA': os.environ.get('PASTA_AMERICA_ID'),
            'ASIA': os.environ.get('PASTA_ASIA_ID'),
            'EUROPA': os.environ.get('PASTA_EUROPA_ID'),
            'BANDEIRAS': os.environ.get('PASTA_BANDEIRAS_ID')
        }

        pasta_id = pasta_drive_map.get(tipo_operacao.upper())
        if not pasta_id:
            logger.error(f"❌ Tipo de operação '{tipo_operacao}' não encontrado no mapeamento.")
            return None

        # Busca pelo arquivo
        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logger.error(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta de {tipo_operacao}.")
            return None

        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)

        caminho_completo = os.path.join(destino_pasta, nome_arquivo)

        fh = io.FileIO(caminho_completo, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            if status:
                logger.info(f"⬇️ Download {int(status.progress() * 100)}% concluído.")

        logger.info(f"✅ Arquivo '{nome_arquivo}' baixado e salvo em '{caminho_completo}'.")
        return caminho_completo

    except Exception as e:
        logger.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return None
