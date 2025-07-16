import os
import io
import requests
import gspread
from PIL import Image, ImageDraw, ImageFont
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from telegram import Bot
from datetime import datetime

# ========== CONFIGURAÇÕES ==========
GOOGLE_SHEET_CREDENTIALS = 'credentials.json'
SPREADSHEET_CLIENTES = 'Fallah_Clientes_Oficial'
SPREADSHEET_OPERACOES = 'Fallah_Operacoes_Oficial'
TELEGRAM_BOT_TOKEN = 'SEU_TOKEN_TELEGRAM'
ESCUDOS_FOLDER_ID = '1KXxOkpbxWvxekEA1AgqW1ho25gXzLv4R'
MATRIZ_BACK_FILE_ID = '1JqLQ4kdDNlUtei7AFVFmKv9fj-ZvZlSc'
STORAGE_DIR = 'temp_files'

# ========== FUNÇÕES AUXILIARES ==========
def autenticar_google():
    escopo = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credenciais = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEET_CREDENTIALS, escopo)
    cliente = gspread.authorize(credenciais)
    drive = build('drive', 'v3', credentials=credenciais)
    return cliente, drive

def obter_clientes_ativos(cliente):
    plan = cliente.open(SPREADSHEET_CLIENTES).sheet1
    dados = plan.get_all_records()
    return [linha['CHAT_ID'] for linha in dados if linha['STATUS'].strip().upper() == 'ATIVO']

def baixar_arquivo_drive(drive, file_id, nome_arquivo):
    request = drive.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    with open(os.path.join(STORAGE_DIR, nome_arquivo), 'wb') as f:
        f.write(fh.read())

def buscar_escudo_url(time):
    response = requests.get(f"https://api.sofascore.com/api/v1/search/multi?q={time}")
    try:
        resultados = response.json().get('teams', {}).get('data', [])
        for t in resultados:
            if time.lower() in t['name'].lower():
                return f"https://api.sofascore.app/api/v1/team/{t['id']}/image"
    except:
        return None
    return None

def buscar_info_jogo():
    return {
        "estadio": "Allianz Parque",
        "competicao": "Brasileirão Betano",
        "horario": "19:00",
        "mercado": "Back Palmeiras",
        "odds": "1.42",
        "stake": "R$100",
        "liquidez": "R$2826",
        "time_casa": "Palmeiras",
        "time_visitante": "Mirassol"
    }

def gerar_imagem(jogo_info, matriz_path, escudo_casa, escudo_visitante):
    base = Image.open(matriz_path).convert("RGBA")
    draw = ImageDraw.Draw(base)
    fonte = ImageFont.truetype("arial.ttf", 26)

    draw.text((220, 350), jogo_info['estadio'], font=fonte, fill="black")
    draw.text((220, 390), jogo_info['competicao'], font=fonte, fill="black")
    draw.text((220, 430), jogo_info['odds'], font=fonte, fill="black")
    draw.text((220, 470), jogo_info['stake'], font=fonte, fill="black")
    draw.text((220, 510), jogo_info['mercado'], font=fonte, fill="black")
    draw.text((220, 550), jogo_info['liquidez'], font=fonte, fill="black")
    draw.text((220, 590), jogo_info['horario'], font=fonte, fill="black")

    escudo1 = Image.open(escudo_casa).resize((70, 70))
    escudo2 = Image.open(escudo_visitante).resize((70, 70))
    base.paste(escudo1, (60, 200), escudo1)
    base.paste(escudo2, (360, 200), escudo2)

    caminho_final = os.path.join(STORAGE_DIR, "imagem_final.png")
    base.save(caminho_final)
    return caminho_final

def enviar_imagem(bot_token, chat_id, caminho_imagem):
    bot = Bot(token=bot_token)
    with open(caminho_imagem, "rb") as f:
        bot.send_photo(chat_id=chat_id, photo=f)

# ========== EXECUÇÃO PRINCIPAL ==========
if __name__ == "__main__":
    os.makedirs(STORAGE_DIR, exist_ok=True)
    cliente, drive = autenticar_google()
    clientes_ativos = obter_clientes_ativos(cliente)

    jogo = buscar_info_jogo()
    baixar_arquivo_drive(drive, MATRIZ_BACK_FILE_ID, "matriz.png")

    url_escudo_casa = buscar_escudo_url(jogo['time_casa'])
    url_escudo_visitante = buscar_escudo_url(jogo['time_visitante'])

    escudo_caminho1 = os.path.join(STORAGE_DIR, "casa.png")
    escudo_caminho2 = os.path.join(STORAGE_DIR, "visitante.png")

    with open(escudo_caminho1, 'wb') as f:
        f.write(requests.get(url_escudo_casa).content)
    with open(escudo_caminho2, 'wb') as f:
        f.write(requests.get(url_escudo_visitante).content)

    imagem = gerar_imagem(jogo, os.path.join(STORAGE_DIR, "matriz.png"), escudo_caminho1, escudo_caminho2)

    for chat_id in clientes_ativos:
        enviar_imagem(TELEGRAM_BOT_TOKEN, chat_id, imagem)

    print("Imagem gerada e enviada com sucesso.")
