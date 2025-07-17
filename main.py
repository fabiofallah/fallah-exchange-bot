import os, io
import gspread
from google.oauth2 import service_account
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Configurações via env
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
CREDS_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
FOLDER_ENTRADA = os.environ['PASTA_ENTRADA_ID']
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

# Autorizações
creds = service_account.Credentials.from_service_account_info(
    json.loads(CREDS_JSON), scopes=SCOPES
)
gdrive = build('drive', 'v3', credentials=creds)
gsheets = gspread.authorize(creds)
bot = Bot(token=TELEGRAM_TOKEN)

def buscar_dados_planilha():
    sheet = gsheets.open_by_key(SPREADSHEET_ID).worksheet('Fallah_Clientes_Oficial')
    return sheet.get_all_records()

def buscar_imagem_e_enviar(dados):
    # busca imagem na pasta entrada
    resp = gdrive.files().list(
        q=f"'{FOLDER_ENTRADA}' in parents and mimeType contains 'image/'",
        pageSize=1, fields="files(id, name)"
    ).execute()
    files = resp.get('files', [])
    if not files: return
    fid, fname = files[0]['id'], files[0]['name']
    buf = io.BytesIO()
    request = gdrive.files().get_media(fileId=fid)
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 28)
    draw.text((50,50), f"👤 Cliente: {dados[0]['NOME']}", font=font, fill='white')
    # outras legendas...
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    bot.send_photo(chat_id=CHAT_ID, photo=bio, caption="✅ Entrada")
    print("✔️ Enviado")

def main():
    dados = buscar_dados_planilha()
    if not dados: return
    buscar_imagem_e_enviar(dados)

if __name__ == '__main__':
    main()
