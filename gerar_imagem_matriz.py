import os
import io
import cv2
import numpy as np
from googleapiclient.discovery import build
from google.oauth2 import service_account
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

# Scopes e variáveis de ambiente
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
CRED_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
ENTRADA_ID = os.getenv('PASTA_ENTRADA_ID')
ESCUDOS_ID = os.getenv('PASTA_ESCUDOS_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.getenv('TELEGRAM_CHAT_ID')

# Verificação de variáveis obrigatórias
for name, val in [
    ('GOOGLE_CREDENTIALS_JSON', CRED_JSON),
    ('PASTA_ENTRADA_ID', ENTRADA_ID),
    ('PASTA_ESCUDOS_ID', ESCUDOS_ID),
    ('TELEGRAM_BOT_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT),
]:
    if not val:
        logging.error(f'Variável de ambiente ausente: {name}; finalize antes de prosseguir.')
        exit(1)

# Inicia Google Drive, Sheets e Telegram
creds = service_account.Credentials.from_service_account_info(eval(CRED_JSON), scopes=SCOPES)
drive = build('drive', 'v3', credentials=creds)
bot = Bot(TELEGRAM_TOKEN)

def baixar_escudo(nome_time):
    q = f"'{ESCUDOS_ID}' in parents and name contains '{nome_time}'"
    resp = drive.files().list(q=q, fields='files(id,name)').execute()
    files = resp.get('files', [])
    if not files:
        logging.warning(f'Escudo "{nome_time}" não encontrado em pasta de escudos.')
        return None
    file = files[0]
    data = drive.files().get_media(fileId=file['id']).execute()
    buf = io.BytesIO(data)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
    return img

def gerar_e_enviar():
    # Exemplo: dados fictícios, ajuste conforme seu ler_entrada()
    entrada = { 'Time_Casa': 'Flamengo', 'Time_Visitante': 'Fluminense',
                'Odds': '1.95', 'Stake': '5', 'Liquidez': '200', 'Hora': '19:30',
                'Competicao': 'Brasileirao', 'Estadio': 'Maracana' }
    template = baixar_escudo(entrada['Time_Casa'])  # ou o nome da matriz
    # ... restaura processamento, inserção de textos e escudos ...
    out = 'matriz_entrada_preenchida.png'
    cv2.imwrite(out, template)  # substitua template pelo mat
    logging.info('Imagem gerada. Enviando Telegram...')
    try:
        bot.send_photo(chat_id=TELEGRAM_CHAT, photo=open(out, 'rb'))
        logging.info('✅ Entrada enviada.')
    except Exception as e:
        logging.error('❌ Erro ao enviar ao Telegram:', exc_info=e)

if __name__ == '__main__':
    gerar_e_enviar()

