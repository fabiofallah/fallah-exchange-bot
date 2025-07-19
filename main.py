import os
import json
import gspread
from google.oauth2.service_account import Credentials

def parse_google_json_env():
    raw_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if not raw_json:
        raise SystemExit("❌ GOOGLE_CREDENTIALS_JSON está vazio!")

    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        fixed_json = raw_json.replace("\\n", "\n").replace('\\"', '"')
        return json.loads(fixed_json)

# Autenticação
creds_dict = parse_google_json_env()
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

try:
    print("📘 Acessando planilha...")
    sheet = gc.open_by_key(SPREADSHEET_ID).worksheet("CPF_ROBOTICO")  # ABA CORRETA AQUI
    print("✅ Planilha encontrada!")
    print(f"📄 Título: {sheet.title}")
except Exception as e:
    print(f"❌ Erro ao acessar a planilha: {e}")
