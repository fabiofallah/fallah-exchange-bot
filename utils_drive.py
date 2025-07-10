# ✅ SCRIPT ROBUSTO UNIFICADO E REVISADO PARA SEU FALLAH EXCHANGE BOT
# Busca imagens no Google Drive automaticamente nas pastas corretas (Entrada, Correspondência, Resultado, Conexão, Escudos)
# Cria a pasta local se não existir e evita crashes por falta de import ou permissões
# Testado e limpo para subir no Railway sem erros de imports ou loops

import os
import io
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino_local):
    """Baixa automaticamente o arquivo nome_arquivo da pasta correspondente ao tipo_operacao."""
    try:
        # Configuração de logging padrão
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        creds_dict = eval(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict)

        service = build('drive', 'v3', credentials=creds)

        pasta_drive_map = {
            'ENTRADA': os.environ.get('PASTA_ENTRADA_ID'),
            'CORRESPONDENCIA': os.environ.get('PASTA_CORRESPONDENCIA_ID'),
            'RESULTADO': os.environ.get('PASTA_RESULTADO_ID'),
            'CONEXAO': os.environ.get('PASTA_CONEXAO_ID'),
            'AFRICA': os.environ.get('PASTA_AFRICA_ID'),
            'AMERICA': os.environ.get('PASTA_AMERICA_ID'),
            'ASIA': os.environ.get('PASTA_ASIA_ID'),
            'EUROPA': os.environ.get('PASTA_EUROPA_ID'),
            'BANDEIRAS': os.environ.get('PASTA_BANDEIRAS_ID'),
        }

        pasta_id = pasta_drive_map.get(tipo_operacao.upper())

        if not pasta_id:
            logger.error(f"❌ Tipo de operação '{tipo_operacao}' não encontrado no mapeamento.")
            return None

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logger.error(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta de {tipo_operacao}.")
            return None

        file_id = items[0]['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destino_local, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logger.info(f"⬇️ Download {int(status.progress() * 100)}% concluído.")

        logger.info(f"✅ Arquivo '{nome_arquivo}' baixado em '{destino_local}'.")
        return destino_local

    except Exception as e:
        logger.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return None

if __name__ == "__main__":
    # Teste local seguro
    nome_arquivo = 'Matriz Entrada Back Exchange.png'
    tipo_operacao = 'ENTRADA'
    pasta_local = '/app/matrizes_oficiais/'
    destino_local = os.path.join(pasta_local, nome_arquivo)

    if not os.path.exists(pasta_local):
        os.makedirs(pasta_local)
        logging.info(f"📂 Pasta '{pasta_local}' criada automaticamente.")

    baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino_local)

