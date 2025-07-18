import os
import logging
import json
from io import BytesIO
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from google.oauth2.service_account import Credentials
import gspread
from PIL import Image

# Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente obrigatórias
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
FOLDER_ENTRADA_ID = os.getenv('PASTA_ENTRADA_ID')

# Verificações iniciais
required = {
    'TELEGRAM_BOT_TOKEN': TELEGRAM_TOKEN,
    'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    'GOOGLE_CREDENTIALS_JSON': GOOGLE_CREDENTIALS,
    'SPREADSHEET_ID': SPREADSHEET_ID,
    'PASTA_ENTRADA_ID': FOLDER_ENTRADA_ID
}
for name, val in required.items():
    if not val:
        logger.error(f"⚠️ Variável obrigatória ausente: {name}")
        raise SystemExit(f"Erro: falta {name}")

# Conexão com Google Sheets/Drive
creds_info = json.loads(GOOGLE_CREDENTIALS)
scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
gc = gspread.authorize(creds)

# Conexão com Telegram
bot = Bot(token=TELEGRAM_TOKEN)

def buscar_entrada():
    sheet = gc.open_by_key(SPREADSHEET_ID).worksheet('Fallah_Clientes_Oficial')
    # Supondo colunas fixas na mesma ordem do print:
    # A: CPF_ROBOTICO, B: NOME, C: CHAT_ID, D: STATUS, E: PLANO, F: DATA_INICIO, G: DATA_FIM, H: OBSERVACOES
    rows = sheet.get_all_records()
    return rows

def enviar_mensagem(dados):
    for item in dados:
        chat_id = item.get('CHAT_ID')
        if not chat_id:
            continue
        texto = (
            f"*Oferta encontrada!*\n"
            f"Cliente: {item['NOME']}\n"
            f"Plano: {item['PLANO']}\n"
            f"Status: {item['STATUS']}\n"
            f"Início/Fim: {item['DATA_INICIO']} → {item['DATA_FIM']}"
        )
        bot.send_message(chat_id=chat_id, text=texto, parse_mode='Markdown')

def main():
    logger.info("🔄 Iniciando consulta de entradas...")
    dados = buscar_entrada()
    if not dados:
        logger.info("Nenhuma entrada encontrada.")
    else:
        enviar_mensagem(dados)
        logger.info(f"{len(dados)} mensagens enviadas.")

if __name__ == '__main__':
    main()
