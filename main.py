import os
import gspread
import requests
from google.oauth2.service_account import Credentials
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# ======================= VARIÁVEIS DE AMBIENTE =======================
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
GOOGLE_CREDENTIALS_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
GOOGLE_SHEET_ID = os.environ['GOOGLE_SHEET_ID']
FOLDER_ENTRADA_ID = os.environ['FOLDER_ENTRADA_ID']
# =====================================================================

# Inicializa o bot do Telegram
bot = Bot(token=TELEGRAM_TOKEN)

# Carrega credenciais do Google via JSON da variável de ambiente
import json
info = json.loads(GOOGLE_CREDENTIALS_JSON)
creds = Credentials.from_service_account_info(info)
gc = gspread.authorize(creds)

# Acessa a planilha
sheet = gc.open_by_key(GOOGLE_SHEET_ID)
worksheet = sheet.get_worksheet(0)
dados = worksheet.get_all_records()

# Filtra clientes ativos e com plano PRÓ
chat_ids = [str(row["CHAT_ID"]) for row in dados if row["STATUS"].upper() == "ATIVO" and row["PLANO"].upper() == "PRÓ"]

# Função para obter o nome do arquivo mais recente da pasta de entrada no Drive
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

drive_service = build("drive", "v3", credentials=creds)

def baixar_ultima_imagem_da_pasta(pasta_id, nome_local):
    resultados = drive_service.files().list(
        q=f"'{pasta_id}' in parents and mimeType contains 'image/'",
        orderBy="createdTime desc",
        pageSize=1,
        fields="files(id, name)"
    ).execute()

    arquivos = resultados.get("files", [])
    if not arquivos:
        print("Nenhuma imagem encontrada na pasta de entrada.")
        return None

    file_id = arquivos[0]["id"]
    nome_original = arquivos[0]["name"]

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(nome_local, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    print(f"Imagem {nome_original} baixada como {nome_local}")
    return nome_local

# Caminho local temporário
caminho_imagem_local = "imagem_entrada.png"
imagem_baixada = baixar_ultima_imagem_da_pasta(FOLDER_ENTRADA_ID, caminho_imagem_local)

# Envia a imagem para os clientes válidos
if imagem_baixada:
    for chat_id in chat_ids:
        try:
            bot.send_photo(chat_id=chat_id, photo=open(caminho_imagem_local, 'rb'))
            print(f"✅ Imagem enviada para {chat_id}")
        except Exception as e:
            print(f"❌ Erro ao enviar imagem para {chat_id}: {e}")
else:
    print("❌ Nenhuma imagem para enviar.")

