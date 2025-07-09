import os
import io
import json
import logging
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

# IDs das pastas e arquivo no Drive
PASTA_ENTRADA_ID = '1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz'  # Pasta de ENTRADA
ARQUIVO_ENTRADA = 'Matriz Entrada Back Exchange.png'

# Dados do evento PSG x Real Madrid
dados_entrada = {
    'estadio': 'MetLife Stadium',
    'competicao': 'FIFA Club World Cup - Semifinal',
    'odds': '2.44',
    'stake': 'R$100,00',
    'mercado': 'BACK PSG',
    'liquidez': '450K',
    'horario': '16:00',
    'resultado': '-'  # Entrada ainda em andamento
}

def baixar_arquivo_drive(service, file_name, folder_id, local_file):
    results = service.files().list(q=f"'{folder_id}' in parents and name='{file_name}'",
                                   spaces='drive',
                                   fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        raise FileNotFoundError(f"Arquivo {file_name} não encontrado na pasta do Drive.")
    file_id = items[0]['id']
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_file, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    logger.info(f"Download do arquivo {file_name} concluído.")

def preencher_matriz():
    image = Image.open('matriz_entrada.png').convert('RGBA')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Inserir dados no card
    draw.text((160, 310), dados_entrada['estadio'], fill='black', font=font)
    draw.text((160, 360), dados_entrada['competicao'], fill='black', font=font)
    draw.text((160, 410), dados_entrada['odds'], fill='black', font=font)
    draw.text((160, 460), dados_entrada['stake'], fill='black', font=font)
    draw.text((160, 510), dados_entrada['mercado'], fill='black', font=font)
    draw.text((160, 560), dados_entrada['liquidez'], fill='black', font=font)
    draw.text((160, 610), dados_entrada['horario'], fill='black', font=font)
    draw.text((160, 660), dados_entrada['resultado'], fill='black', font=font)

    # Inserir escudos nos retângulos (substitua pelos caminhos corretos caso queira os logos)
    # escudo_casa = Image.open('escudos/psg.png').resize((150, 150))
    # escudo_fora = Image.open('escudos/real_madrid.png').resize((150, 150))
    # image.paste(escudo_casa, (40, 100))
    # image.paste(escudo_fora, (460, 100))

    image.save('matriz_entrada_pronta.png')
    logger.info("Imagem da matriz preenchida gerada com sucesso.")

async def main():
    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)

    # Baixar a matriz do Drive
    request = service.files().list(q=f"'{PASTA_ENTRADA_ID}' in parents and name='{ARQUIVO_ENTRADA}'", spaces='drive').execute()
    file_id = request['files'][0]['id']
    request_file = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request_file)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with open('matriz_entrada.png', 'wb') as f:
        f.write(fh.getbuffer())
    logger.info("Arquivo matriz_entrada.png baixado do Drive.")

    preencher_matriz()

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open('matriz_entrada_pronta.png', 'rb') as photo:
        await bot.send_photo(chat_id=CHAT_ID, photo=photo)
    logger.info("Imagem enviada ao Telegram com sucesso.")

if __name__ == '__main__':
    asyncio.run(main())

