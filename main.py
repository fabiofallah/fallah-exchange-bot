import os
import logging
import telebot
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# --- Variáveis de Ambiente (usando exatamente os nomes que você usou no Railway) ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
GOOGLE_CREDENTIALS_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
PASTA_ENTRADA_ID = os.environ['PASTA_ENTRADA_ID']
PASTA_ESCUDOS_ID = os.environ['PASTA_ESCUDOS_ID']
PASTA_RESULTADO_ID = os.environ['PASTA_RESULTADO_ID']
PASTA_CORRESPONDENCIA_ID = os.environ['PASTA_CORRESPONDENCIA_ID']
PASTA_CONEXAO_ID = os.environ['PASTA_CONEXAO_ID']

# --- Inicializa o Bot ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- Configura Credenciais Google ---
import json
import tempfile

with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp:
    temp.write(GOOGLE_CREDENTIALS_JSON.encode())
    temp.flush()
    credentials = service_account.Credentials.from_service_account_file(temp.name)
    drive_service = build('drive', 'v3', credentials=credentials)
    sheets_service = build('sheets', 'v4', credentials=credentials)

# --- Função: Buscar Dados da Planilha ---
def buscar_dados_planilha():
    range_name = 'Página1!A2:G2'  # Ajuste conforme sua planilha
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()
    valores = result.get('values', [])
    if not valores or not valores[0]:
        return None
    return valores[0]

# --- Função: Baixar escudo por nome (busca por aproximação) ---
def buscar_escudo_por_nome(nome_time):
    query = f"'{PASTA_ESCUDOS_ID}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    arquivos = results.get('files', [])
    nome_normalizado = nome_time.strip().lower()
    for arquivo in arquivos:
        if nome_normalizado in arquivo['name'].strip().lower():
            return arquivo['id']
    return None

# --- Função: Baixar imagem do Drive por ID ---
def baixar_imagem_por_id(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return Image.open(fh).convert("RGBA")

# --- Função: Gerar imagem final com dados e escudos ---
def gerar_imagem_matriz_back(dados):
    if not dados or len(dados) < 7:
        raise ValueError("Dados incompletos para gerar imagem.")

    time_casa, time_fora, campeonato, estadio, horario, odd, mercado = dados

    matriz_id = buscar_escudo_por_nome("matriz_back")  # ID da imagem base
    if not matriz_id:
        raise Exception("Imagem base 'matriz_back' não encontrada.")
    imagem_base = baixar_imagem_por_id(matriz_id).copy()

    # Fontes
    fonte_padrao = ImageFont.truetype("arial.ttf", 40)
    draw = ImageDraw.Draw(imagem_base)

    # Texto (posições são exemplo, ajuste conforme seu layout)
    draw.text((80, 60), time_casa.upper(), font=fonte_padrao, fill="white")
    draw.text((80, 120), time_fora.upper(), font=fonte_padrao, fill="white")
    draw.text((80, 180), campeonato.upper(), font=fonte_padrao, fill="white")
    draw.text((80, 240), estadio.upper(), font=fonte_padrao, fill="white")
    draw.text((80, 300), horario.upper(), font=fonte_padrao, fill="white")
    draw.text((80, 360), f"ODD: {odd}", font=fonte_padrao, fill="white")
    draw.text((80, 420), mercado.upper(), font=fonte_padrao, fill="white")

    # Escudos
    escudo_casa_id = buscar_escudo_por_nome(time_casa)
    escudo_fora_id = buscar_escudo_por_nome(time_fora)
    if escudo_casa_id:
        escudo_casa = baixar_imagem_por_id(escudo_casa_id).resize((120, 120))
        imagem_base.paste(escudo_casa, (850, 50), escudo_casa)
    if escudo_fora_id:
        escudo_fora = baixar_imagem_por_id(escudo_fora_id).resize((120, 120))
        imagem_base.paste(escudo_fora, (850, 200), escudo_fora)

    return imagem_base

# --- Função: Enviar imagem no Telegram ---
def enviar_imagem_telegram(img):
    bio = BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    bot.send_photo(CHAT_ID, photo=bio)

# --- Execução principal ---
if __name__ == "__main__":
    try:
        dados = buscar_dados_planilha()
        if not dados:
            raise Exception("Sem dados na planilha.")
        imagem = gerar_imagem_matriz_back(dados)
        enviar_imagem_telegram(imagem)
        print("✅ Imagem enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro: {e}")
        bot.send_message(CHAT_ID, f"⚠️ Erro ao gerar imagem: {e}")
