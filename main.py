import os
import logging
import json
import time
import schedule
from telegram import Bot
import gspread
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def parse_google_json_env():
    raw_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if not raw_json:
        raise SystemExit("❌ GOOGLE_CREDENTIALS_JSON está vazio!")
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        fixed_json = raw_json.replace("\\n", "\n").replace('\\"', '"')
        return json.loads(fixed_json)

creds_dict = parse_google_json_env()
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)

bot = Bot(token=TELEGRAM_TOKEN)

def check_entries():
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID).get_worksheet(0)
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
