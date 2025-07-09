import os
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot

# Configurações iniciais
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_INFO = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

# IDs das pastas
PASTA_ENTRADA_ID = '1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz'
PASTA_ESCUDOS_ID = 'ID_DA_PASTA_DE_ESCUDOS'  # Substituir pelo ID real

# Dados da operação
dados_operacao = {
    "time_casa": "PSG",
    "time_fora": "Real Madrid",
    "estadio": "MetLife Stadium",
    "competicao": "FIFA Club World Cup Semifinal",
    "odds": "2.44",
    "stake": "R$100",
    "mercado": "Back PSG",
    "liquidez": "450K",
    "horario": "16:00",
    "resultado": "Aguardando"
}

# Autenticação com Google Drive
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def baixar_arquivo_drive(file_name, folder_id, local_path):
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        logging.error(f"Arquivo {file_name} não encontrado.")
        return None
    file_id = items[0]['id']
    request = service.files().get_media(fileId=file_id)
    with open(local_path, 'wb') as f:
        downloader = build('drive', 'v3', credentials=credentials).files().get_media(fileId=file_id)
        downloader.execute(fd=f)
    logging.info(f"{file_name} baixado com sucesso.")
    return local_path

def preencher_matriz():
    # Baixar matriz de entrada
    matriz_path = baixar_arquivo_drive('Matriz Entrada Back Exchange.png', PASTA_ENTRADA_ID, 'matriz_entrada.png')
    if not matriz_path:
        return
    # Baixar escudos
    escudo_casa = baixar_arquivo_drive(f'{dados_operacao["time_casa"]}.png', PASTA_ESCUDOS_ID, 'escudo_casa.png')
    escudo_fora = baixar_arquivo_drive(f'{dados_operacao["time_fora"]}.png', PASTA_ESCUDOS_ID, 'escudo_fora.png')

    img = Image.open(matriz_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 48)

    # Posicionar escudos
    if escudo_casa:
        escudo_c = Image.open(escudo_casa).resize((150, 150))
        img.paste(escudo_c, (60, 150), escudo_c)
    if escudo_fora:
        escudo_f = Image.open(escudo_fora).resize((150, 150))
        img.paste(escudo_f, (560, 150), escudo_f)

    # Inserir textos
    draw.text((100, 500), f"{dados_operacao['estadio']}", fill="black", font=font)
    draw.text((100, 570), f"{dados_operacao['competicao']}", fill="black", font=font)
    draw.text((100, 640), f"Odds: {dados_operacao['odds']}", fill="black", font=font)
    draw.text((100, 710), f"Stake: {dados_operacao['stake']}", fill="black", font=font)
    draw.text((100, 780), f"Mercado: {dados_operacao['mercado']}", fill="black", font=font)
    draw.text((100, 850), f"Liquidez: {dados_operacao['liquidez']}", fill="black", font=font)
    draw.text((100, 920), f"Horário: {dados_operacao['horario']}", fill="black", font=font)
    draw.text((100, 990), f"Resultado: {dados_operacao['resultado']}", fill="black", font=font)

    img.save('matriz_final.png')
    logging.info("Matriz preenchida com sucesso.")

def enviar_telegram():
    with open('matriz_final.png', 'rb') as photo:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
    logging.info("Imagem enviada ao Telegram.")

if __name__ == "__main__":
    preencher_matriz()
    enviar_telegram()
