import os
import json
import telegram
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload

# Carrega as credenciais do Railway via variável de ambiente
service_account_info = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
creds = service_account.Credentials.from_service_account_info(service_account_info)

# IDs das planilhas e intervalo da primeira operação real
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
RANGE_NAME = "ENTRADA!A2:J2"  # Uma linha apenas para teste

# Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Sheets API
sheets_service = build('sheets', 'v4', credentials=creds)
sheet = sheets_service.spreadsheets()

# Lê os dados do jogo
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print("Nenhum dado encontrado.")
    exit()

dados = values[0]
(estadio, campeonato, odds, stake, mercado, liquidez, horario, resultado, time1, time2) = dados

# Busca imagem da matriz no Drive
pasta_entrada_id = os.environ["PASTA_ENTRADA_ID"]
arquivos = drive_service.files().list(q=f"'{pasta_entrada_id}' in parents and name contains 'Matriz Entrada Back'", fields="files(id, name)").execute()
arquivo = arquivos.get("files", [])[0]
file_id = arquivo["id"]
request = drive_service.files().get_media(fileId=file_id)
fh = BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while not done:
    status, done = downloader.next_chunk()

fh.seek(0)
imagem = Image.open(fh)

# Fonte
fonte = ImageFont.truetype("arial.ttf", 30)
draw = ImageDraw.Draw(imagem)

# Preenche os campos
draw.text((380, 102), estadio, font=fonte, fill="black")
draw.text((380, 140), campeonato, font=fonte, fill="black")
draw.text((380, 177), odds, font=fonte, fill="black")
draw.text((380, 215), stake, font=fonte, fill="black")
draw.text((380, 252), mercado, font=fonte, fill="black")
draw.text((380, 290), liquidez, font=fonte, fill="black")
draw.text((380, 328), horario, font=fonte, fill="black")
draw.text((380, 367), resultado, font=fonte, fill="black")

# Busca os escudos
def buscar_escudo_por_nome(nome_time):
    pasta_escudos_id = os.environ["PASTA_ESCUDOS_ID"]
    resultado = drive_service.files().list(
        q=f"'{pasta_escudos_id}' in parents and name contains '{nome_time}'",
        fields="files(id, name)"
    ).execute()
    arquivos = resultado.get("files", [])
    if arquivos:
        escudo_id = arquivos[0]["id"]
        request = drive_service.files().get_media(fileId=escudo_id)
        escudo_fh = BytesIO()
        downloader = MediaIoBaseDownload(escudo_fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        escudo_fh.seek(0)
        return Image.open(escudo_fh).convert("RGBA")
    return None

escudo1 = buscar_escudo_por_nome(time1)
escudo2 = buscar_escudo_por_nome(time2)

if escudo1:
    imagem.paste(escudo1.resize((80, 80)), (105, 22), escudo1)
if escudo2:
    imagem.paste(escudo2.resize((80, 80)), (435, 22), escudo2)

# Salva imagem
imagem_final = "/tmp/entrada_pronta.png"
imagem.save(imagem_final)

# Envia no Telegram
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
chat_id = os.environ["CHAT_ID"]
bot.send_photo(chat_id=chat_id, photo=open(imagem_final, 'rb'))
