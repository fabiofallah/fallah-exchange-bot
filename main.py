import os
import logging
import json
from telegram import Bot
import gspread
from google.oauth2.service_account import Credentials

# variáveis de ambiente
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_CREDS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

# validação
for name, val in [('TELEGRAM_BOT_TOKEN', TELEGRAM_TOKEN),
                  ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
                  ('GOOGLE_CREDENTIALS_JSON', GOOGLE_CREDS_JSON),
                  ('SPREADSHEET_ID', SPREADSHEET_ID)]:
    if not val:
        logging.error(f"Falta variável: {name}")
        raise SystemExit(f"Falta variável: {name}")

# autenticação Google
creds_dict = json.loads(GOOGLE_CREDS_JSON)
gc = gspread.service_account_from_dict(creds_dict)

# bot Telegram
bot = Bot(token=TELEGRAM_TOKEN)
