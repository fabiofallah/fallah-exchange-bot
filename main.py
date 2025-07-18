import os, time, logging, json
from telegram import Bot
import gspread
from google.oauth2.service_account import Credentials
import schedule

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente obrigatórias:
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_CREDS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

for name, val in [
    ('TELEGRAM_BOT_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    ('GOOGLE_CREDENTIALS_JSON', GOOGLE_CREDS_JSON),
    ('SPREADSHEET_ID', SPREADSHEET_ID),
]:
    if not val:
        logger.error(f"Falta variável: {name}")
        raise SystemExit

# Autenticação Google
creds_dict = json.loads(GOOGLE_CREDS_JSON)
gc = gspread.service_account_from_dict(creds_dict)

# Bot Telegram
bot = Bot(token=TELEGRAM_TOKEN)

def check_entries():
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID).worksheet('Fallah_Clientes_Oficial')
        rows = sheet.get_all_records()
    except Exception as e:
        logger.error("Erro ao buscar dados da planilha", exc_info=e)
        return

    if not rows:
        logger.info("Nenhuma entrada encontrada.")
        return

    for item in rows:
        chat_id = item.get('CHAT_ID')
        if not chat_id:
            continue

        texto = (
            f"*Oferta encontrada!* \n"
            f"Cliente: {item.get('NOME')}\n"
            f"Plano: {item.get('PLANO')}\n"
            f"Status: {item.get('STATUS')}\n"
            f"Início/Fim: {item.get('DATA_INICIO')} → {item.get('DATA_FIM')}"
        )
        bot.send_message(chat_id=chat_id, text=texto, parse_mode='Markdown')

    logger.info(f"{len(rows)} mensagens enviadas.")

def main():
    logger.info("Scheduler iniciado. Executando a cada 1 min.")
    schedule.every(1).minutes.do(check_entries)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
