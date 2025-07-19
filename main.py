from google.oauth2.service_account import Credentials
import gspread, json

GOOGLE_CREDS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
creds_info = json.loads(GOOGLE_CREDS_JSON)
scopes = [
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
gc = gspread.authorize(creds)

sh = gc.open_by_key(SPREADSHEET_ID)  # aqui deve funcionar
ws = sh.worksheet('Fallah_Clientes_Oficial')
