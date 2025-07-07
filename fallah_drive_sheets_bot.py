import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Escopos necessários para acessar o Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ Carregar credenciais do JSON salvo em variável de ambiente no Railway
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

# Autenticar no Google Sheets
client = gspread.authorize(creds)

# Abrir a planilha pelo nome
spreadsheet = client.open("Fallah Exchange Bets PRO")

# Selecionar a primeira aba
sheet = spreadsheet.sheet1

# Ler os valores da primeira coluna como teste
values = sheet.col_values(1)
print(values)
