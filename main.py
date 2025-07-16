import gspread
import requests
import json
import io
import os
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from telegram import Bot

# === CONFIGURAÇÕES ===
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credenciais.json'
TOKEN_BOT = '7777458509:AAHfshLsxT0dyN30NeY_6zTOnUfQMWJNo58'
ID_PLANILHA_CLIENTES = 'COLE_O_ID_DA_PLANILHA_DE_CLIENTES'
PASTA_ESCUDOS_ID = '1KXxOkpbxWvxekEA1AgqW1ho25gXzLv4R'
ID_IMAGEM_MATRIZ = '1JqLQ4kdDNlUtei7AFVFmKv9fj-ZvZlSc'

# === AUTENTICAÇÃO GOOGLE DRIVE & SHEETS ===
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)
gc = gspread.authorize(creds)

# === COLETA DE CLIENTES ATIVOS ===
sheet = gc.open_by_key(ID_PLANILHA_CLIENTES).sheet1
clientes = sheet.get_all_records()
chat_ids_ativos = [str(c['CHAT_ID']) for c in clientes if c['STATUS'] == 'ATIVO' and c['PLANO'] == 'PRÓ']

# === DADOS DO JOGO VIA SOFASCORE + BETFAIR ===
jogo = {
    "time_casa": "Palmeiras",
    "time_visitante": "Mirassol",
    "estadio": "Allianz Parque",
    "competicao": "Brasileirão Betano",
    "data": "16/07/2025",
    "hora": "19:00",
    "mercado": "Back Palmeiras",
    "odds": "1.43",
    "stake": "R$ 100",
    "liquidez": "R$ 10.793"
}

# === DOWNLOAD DA MATRIZ OFICIAL DO DRIVE ===
request = service.files().get_media(fileId=ID_IMAGEM_MATRIZ)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while not done:
    status, done = downloader.next_chunk()
fh.seek(0)
imagem_base = Image.open(fh).convert("RGBA")

# === FUNÇÃO: BUSCA ESCUDO DO TIME PELO NOME ===
def buscar_escudo_drive(nome_time):
    query = f"'{PASTA_ESCUDOS_ID}' in parents and name contains '{nome_time}' and trashed = false"
    results = service.files().list(q=query, pageSize=5, fields="files(id, name)").execute()
    arquivos = results.get('files', [])
    if not arquivos:
        return None
    file_id = arquivos[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return Image.open(fh).convert("RGBA")

escudo_casa = buscar_escudo_drive(jogo["time_casa"])
escudo_visitante = buscar_escudo_drive(jogo["time_visitante"])

# === INSERÇÃO DAS INFORMAÇÕES NA MATRIZ ===
draw = ImageDraw.Draw(imagem_base)
fonte_padrao = ImageFont.truetype("arial.ttf", 60)

# Estádio
draw.text((150, 660), f"{jogo['estadio']}", fill="white", font=fonte_padrao)

# Odds / Stake
draw.text((230, 200), f"{jogo['odds']}", fill="cyan", font=fonte_padrao)
draw.text((230, 270), f"{jogo['stake']}", fill="white", font=fonte_padrao)

# Times
draw.text((80, 90), f"{jogo['time_casa']} x {jogo['time_visitante']}", fill="white", font=fonte_padrao)

# Horário
draw.text((80, 590), f"{jogo['data']} às {jogo['hora']}", fill="white", font=fonte_padrao)

# Escudos
if escudo_casa:
    imagem_base.paste(escudo_casa.resize((130, 130)), (40, 420), escudo_casa.resize((130, 130)))
if escudo_visitante:
    imagem_base.paste(escudo_visitante.resize((130, 130)), (390, 420), escudo_visitante.resize((130, 130)))

# === SALVAR IMAGEM FINAL ===
imagem_base.save("entrada_final.png")

# === ENVIO NO TELEGRAM PARA CLIENTES ATIVOS ===
bot = Bot(token=TOKEN_BOT)
for chat_id in chat_ids_ativos:
    with open("entrada_final.png", "rb") as imagem:
        bot.send_photo(chat_id=chat_id, photo=imagem, caption="🎯 Entrada Programada\nBack Palmeiras - Brasileirão")

