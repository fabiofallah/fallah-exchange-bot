import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot

# Variáveis de ambiente
GOOGLE_CREDENTIALS_JSON = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Autenticar com Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS_JSON, scope)
gc = gspread.authorize(credentials)

try:
    print("📂 Acessando planilha...")
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    print("✅ Planilha encontrada!")

    worksheet = spreadsheet.sheet1  # acessa a aba padrão (Sheet1)
    print(f"✅ Aba '{worksheet.title}' acessada com sucesso!")

    # Ler os dados
    data = worksheet.get_all_records()
    print("📄 Registros encontrados:", len(data))

    if data:
        first_user = data[0]
        nome = first_user['NOME']
        chat_id = str(first_user['CHAT_ID']).strip()

        mensagem = f"✅ Mensagem enviada para {nome} ({chat_id})"
        print(mensagem)

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=chat_id, text=f"Olá {nome}, seja bem-vindo(a) ao sistema Fallah!")

except Exception as e:
    print(f"❌ Erro ao acessar a planilha ou enviar mensagem: {e}")
