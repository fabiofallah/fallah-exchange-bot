import os
import json
import gspread
import telegram
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

try:
    print("📂 Acessando planilha...")
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    print("✅ Planilha encontrada!")

    # Corrigido: nome da aba precisa ser exatamente CPF_ROBOTICO
    worksheet = spreadsheet.worksheet("CPF_ROBOTICO")
    print("✅ Aba CPF_ROBOTICO acessada com sucesso!")

    # Leitura dos dados da planilha
    data = worksheet.get_all_records()
    print("📊 Registros encontrados:", len(data))

    # Enviar mensagem de boas-vindas ao primeiro cliente (exemplo)
    if data:
        first_user = data[0]
        chat_id = str(first_user['CHAT_ID']).strip()
        nome = first_user['NOME']

        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        mensagem = f"Olá {nome}, você está conectado ao Robô Fallah Oficial com sucesso! 🤖✅"
        bot.send_message(chat_id=chat_id, text=mensagem)
        print(f"📨 Mensagem enviada para {nome} ({chat_id})")

except Exception as e:
    print("❌ Erro ao acessar a planilha:", e)
