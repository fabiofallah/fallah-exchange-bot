import os
import io
import gspread
import requests
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.service_account import Credentials
from telegram import Bot

# === Carregar variáveis do Railway ===
google_credentials_json = os.environ['GOOGLE_CREDENTIALS_JSON']
spreadsheet_id = os.environ['SPREADSHEET_ID']
telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']
pasta_entrada_id = os.environ['PASTA_ENTRADA_ID']

# === Autenticar com Google Sheets ===
import json
creds_dict = json.loads(google_credentials_json)
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# === Ler dados da planilha ===
sheet = client.open_by_key(spreadsheet_id)
worksheet = sheet.get_worksheet(0)
dados = worksheet.get_all_records()

# === Pegar o último jogo preenchido ===
ultimo_jogo = dados[-1]

# === Buscar imagem base da pasta do Drive ===
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

service = build('drive', 'v3', credentials=creds)

# Procurar imagem .png na pasta de entrada
results = service.files().list(
    q=f"'{pasta_entrada_id}' in parents and mimeType='image/png'",
    pageSize=1,
    orderBy="createdTime desc",
    fields="files(id, name)"
).execute()

items = results.get('files', [])
if not items:
    raise Exception("Nenhuma imagem PNG encontrada na pasta de entrada.")

file_id = items[0]['id']
file_name = items[0]['name']

# Baixar imagem da matriz
request = service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while not done:
    status, done = downloader.next_chunk()
fh.seek(0)
image = Image.open(fh).convert("RGBA")

# === Editar a imagem com os dados da planilha ===
draw = ImageDraw.Draw(image)
fonte_padrao = ImageFont.truetype("arial.ttf", size=32)  # você pode trocar para uma fonte custom se preferir

# Posicionar os campos conforme sua matriz visual
draw.text((100, 230), str(ultimo_jogo["ESTÁDIO"]), fill="black", font=fonte_padrao)
draw.text((100, 300), str(ultimo_jogo["COMPETIÇÃO"]), fill="black", font=fonte_padrao)
draw.text((100, 370), str(ultimo_jogo["ODDS"]), fill="black", font=fonte_padrao)
draw.text((100, 440), str(ultimo_jogo["STAKE"]), fill="black", font=fonte_padrao)
draw.text((100, 510), str(ultimo_jogo["MERCADO"]), fill="black", font=fonte_padrao)
draw.text((100, 580), str(ultimo_jogo["LIQUIDEZ"]), fill="black", font=fonte_padrao)
draw.text((100, 650), str(ultimo_jogo["HORÁRIO"]), fill="black", font=fonte_padrao)
draw.text((100, 720), str(ultimo_jogo["RESULTADO"]), fill="black", font=fonte_padrao)

# === Salvar imagem temporária ===
caminho_imagem_editada = "imagem_entrada.png"
image.save(caminho_imagem_editada)

# === Enviar imagem via Telegram ===
bot = Bot(token=telegram_token)
with open(caminho_imagem_editada, "rb") as f:
    bot.send_photo(chat_id=chat_id, photo=f, caption="✅ Entrada gerada com sucesso!")

print("Imagem enviada com sucesso.")
