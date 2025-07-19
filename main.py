import os
import logging
import json
import time
import schedule
from telegram import Bot
import gspread
from google.oauth2.service_account import Credentials

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente obrigatórias
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_CREDS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = 'CPF_ROBOTICO'  # ✅ Nome correto da aba no Google Sheets

# Validação das variáveis
for name, val in [
    ('TELEGRAM_BOT_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    ('GOOGLE_CREDENTIALS_JSON', GOOGLE_CREDS_JSON),
    ('SPREADSHEET_ID', SPREADSHEET_ID)
]:
    if not val:
        logger.error(f"❌ Variável obrigatória ausente: {name}")
        raise SystemExit(f"Erro: falta {name}")

# Autenticação no Google Sheets
creds_dict = json.loads(GOOGLE_CREDS_JSON)
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)

# Bot do Telegram
bot = Bot(token=TELEGRAM_TOKEN)

def check_entries():
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)
        rows = sheet.get_all_records()
        return rows
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados da planilha: {e}")
        return []

def send_messages(entries):
    for item in entries:
        chat_id = item.get('CHAT_ID')
        if not chat_id:
            continue

        texto = (
            f"✅ *Oferta encontrada!*\n"
            f"*Cliente:* {item.get('NOME')}\n"
            f"*Plano:* {item.get('PLANO')}\n"
            f"*Status:* {item.get('STATUS')}\n"
            f"*Início/Fim:* {item.get('DATA_INICIO')} ➜ {item.get('DATA_FIM')}"
        )

        bot.send_message(chat_id=chat_id, text=texto, parse_mode='Markdown')

def job():
    logger.info("🔄 Verificando entradas...")
    entries = check_entries()
    if entries:
        send_messages(entries)
        logger.info(f"✅ {len(entries)} mensagens enviadas.")
    else:
        logger.info("ℹ️ Nenhuma entrada encontrada.")

def main():
    schedule.every(1).minutes.do(job)
    logger.info("🕒 Scheduler iniciado. Executando a cada 1 min.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
