import os, json, gspread
from google.oauth2.service_account import Credentials

GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

scopes = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive'
]
creds_info = json.loads(GOOGLE_CREDS_JSON)
creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
gc = gspread.authorize(creds)

sh = gc.open_by_key(SPREADSHEET_ID)
ws = sh.worksheet("Fallah_Clientes_Oficial")
