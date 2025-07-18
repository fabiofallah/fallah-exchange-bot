import os
import logging
import json
import time
import schedule
import gspread
from telegram import Bot
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_CREDS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

for name, val in [('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
                  ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
                  ('GOOGLE_CREDENTIALS_JSON', GOOGLE_CREDS_JSON),
                  ('SPREADSHEET_ID', SPREADSHEET_ID)]:
    if not val:
        logger.error(f'Falta variável: {name}')
        raise SystemExit(f'Falta variável: {name}')

creds = Credentials.from_service_account_info(json.loads(GOOGLE_CREDS_JSON))
gc = gspread.authorize(creds)
bot = Bot(token=TELEGRAM_TOKEN)

def check_entries():
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID).worksheet('Fallah_Clientes_Oficial')
        rows = sheet.get_all_records()
        if not rows:
            logger.info("Nenhuma entrada encontrada.")
            return
        for item in rows:
            chat_id = item.get('CHAT_ID')
            if not chat_id:
                continue
            texto = (
                f"💡 Oferta encontrada!\n"
                f"Cliente: {item.get('NOME')}\n"
                f"Plano: {item.get('PLANO')}\n"
                f"Status: {item.get('STATUS')}\n"
                f"Início/Fim: {item.get('DATA_INICIO')} → {item.get('DATA_FIM')}"
            )
            bot.send_message(chat_id=chat_id, text=texto, parse_mode='Markdown')
        logger.info(f"{len(rows)} mensagens enviadas.")
    except Exception as e:
        logger.error("Erro ao buscar dados da planilha", exc_info=e)

schedule.every(1).minutes.do(check_entries)

def run_scheduler():
    logger.info("Scheduler iniciado. Executando a cada 1 min.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_scheduler()
