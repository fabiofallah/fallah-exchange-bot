import os
import io
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
import gspread
from telegram import Bot

# Configurações via variáveis de ambiente
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
FOLDER_ENTRADA_ID = os.environ['PASTA_ENTRADA_ID']
GOOGLE_CREDENTIALS_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']

# Autenticação Google Sheets
creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
credentials = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=[
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/spreadsheets'
    ]
)
gc = gspread.authorize(credentials)

def buscar_dados_planilha():
    sh = gc.open_by_key(SPREADSHEET_ID)
    wks = sh.worksheet("Fallah_Clientes_Oficial")  # nome exato da aba
    dados = wks.get_all_records()
    return dados

def autenticar_drive():
    return build('drive', 'v3', credentials=credentials)

def buscar_imagem(service):
    res = service.files().list(
        q=f"'{FOLDER_ENTRADA_ID}' in parents and mimeType='image/png'",
        fields="files(id,name)"
    ).execute()
    files = res.get('files', [])
    if not files:
        raise Exception("Nenhuma imagem PNG na pasta.")
    return files[0]['id'], files[0]['name']

def baixar_imagem(service, file_id):
    resp = service.files().get_media(fileId=file_id).execute()
    img = Image.open(io.BytesIO(resp)).convert('RGB')
    return img

def preencher_imagem(img, dados):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 28)
    d = dados[0]  # assumindo primeira linha
    draw.text((50,430), f"🏟️ ESTÁDIO: {d['ESTÁDIO']}", font=font, fill="black")
    # adicione os demais campos...
    return img

def enviar_telegram(img):
    bot = Bot(token=TELEGRAM_TOKEN)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    bot.send_photo(chat_id=CHAT_ID, photo=buf, caption="✅ Entrada")

def main():
    serv = build('drive','v3', credentials=credentials)
    file_id, name = buscar_imagem(serv)
    img = baixar_imagem(serv, file_id)
    dados = buscar_dados_planilha()
    img2 = preencher_imagem(img, dados)
    enviar_telegram(img2)

if __name__=="__main__":
    main()
