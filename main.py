import os
import json
import logging
import time
import schedule  # 1) agendador

from telegram import Bot
import gspread
from google.oauth2.service_account import Credentials

# 2) variáveis de ambiente
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GOOGLE_CREDS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

for name, val in [('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
                  ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
                  ('GOOGLE_CREDS_JSON', GOOGLE_CREDS_JSON),
                  ('SPREADSHEET_ID', SPREADSHEET_ID)]:
    if not val:
        logging.error(f"Falta variável: {name}")
        raise SystemExit(f"Falta variável: {name}")

# 3) autenticação Google
creds = json.loads(GOOGLE_CREDS_JSON)
gc = gspread.service_account_from_dict(creds)  # :contentReference[oaicite:1]{index=1}

bot = Bot(token=TELEGRAM_TOKEN)

def buscar_entrada():
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID).worksheet('Fallah_Clientes_Oficial')
        return sheet.get_all_records()
    except Exception as e:
        logging.error("Erro ao buscar dados da planilha", exc_info=e)
        return []

def enviar_mensagem(dados):
    for item in dados:
        chat_id = item.get('CHAT_ID')
        if not chat_id:
            continue
        texto = (
            f"*Oferta encontrada!*💡\n"
            f"Cliente: {item.get('NOME')}\n"
            f"Plano: {item.get('PLANO')}\n"
            f"Status: {item.get('STATUS')}\n"
            f"Início/Fim: {item.get('DATA_INICIO')} → {item.get('DATA_FIM')}"
        )
        bot.send_message(chat_id=chat_id, text=texto, parse_mode='Markdown')

def job():
    logging.info("🕓 Iniciando consulta de entradas...")
    dados = buscar_entrada()
    if dados:
        enviar_mensagem(dados)
        logging.info(f"{len(dados)} mensagens enviadas.")
    else:
        logging.info("Nenhuma entrada encontrada.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # 4) agenda diária às 9h00
    schedule.every().day.at("09:00").do(job)  # :contentReference[oaicite:2]{index=2}

    logging.info("Scheduler iniciado. Aguardando 1 minuto entre checks.")
    while True:
        schedule.run_pending()
        time.sleep(60)
