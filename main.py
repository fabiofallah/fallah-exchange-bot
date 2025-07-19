import os
import json
import gspread
import asyncio
from telegram import Bot
from oauth2client.service_account import ServiceAccountCredentials

# Variáveis de ambiente
GOOGLE_CREDENTIALS_JSON = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

# Autenticar com Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS_JSON, scope)
gc = gspread.authorize(credentials)

async def main():
    try:
        print("📂 Acessando planilha...")
        spreadsheet = gc.open_by_key(SPREADSHEET_ID)
        print("✅ Planilha encontrada!")

        worksheet = spreadsheet.get_worksheet(0)
        print(f"✅ Aba '{worksheet.title}' acessada com sucesso!")

        data = worksheet.get_all_records()
        print(f"📋 Registros encontrados: {len(data)}")

        if data:
            first_user = data[0]
            chat_id = str(first_user['CHAT_ID']).strip()
            nome = first_user['NOME']

            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            mensagem = f"Olá {nome}, seu CPF Robótico está ativo! 🤖"
            await bot.send_message(chat_id=chat_id, text=mensagem)
            print(f"📨 Mensagem enviada para {nome} ({chat_id})")

    except Exception as e:
        print(f"❌ Erro ao acessar a planilha ou enviar mensagem: {e}")

# Executar função assíncrona
asyncio.run(main())
