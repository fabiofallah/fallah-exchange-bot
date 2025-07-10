import os
import json
import logging
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont
from utils_drive import baixar_arquivo_drive

# Configurações de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PASTA_ENTRADA_ID = os.environ['PASTA_ENTRADA_ID']  # id da pasta de entrada no Drive

# Função para preencher a matriz
def preencher_matriz(matriz_path):
    # Abre a imagem
    img = Image.open(matriz_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Fonte (ajuste conforme necessário)
    fonte = ImageFont.truetype("arial.ttf", 30)

    # Informações para preencher
    estadio = "MetLife Stadium"
    competicao = "Super Mundial Clubes FIFA"
    odds = "2.44"
    stake = "R$ 100"
    mercado = "BACK PSG"
    liquidez = "450K"
    horario = "16:00"
    resultado = "-"

    # Posições aproximadas (ajuste conforme a sua matriz)
    draw.text((100, 500), f"{estadio}", font=fonte, fill="black")
    draw.text((100, 550), f"{competicao}", font=fonte, fill="black")
    draw.text((100, 600), f"{odds}", font=fonte, fill="black")
    draw.text((100, 650), f"{stake}", font=fonte, fill="black")
    draw.text((100, 700), f"{mercado}", font=fonte, fill="black")
    draw.text((100, 750), f"{liquidez}", font=fonte, fill="black")
    draw.text((100, 800), f"{horario}", font=fonte, fill="black")
    draw.text((100, 850), f"{resultado}", font=fonte, fill="black")

    # Salva a imagem preenchida
    output_path = "matriz_entrada_preenchida.png"
    img.save(output_path)
    logger.info("Imagem da matriz preenchida gerada com sucesso.")
    return output_path

# Função principal de execução
async def main():
    logger.info("Iniciando envio automático da matriz de ENTRADA...")

    matriz_nome_drive = "Matriz Entrada Back Exchange.png"
    matriz_nome_local = "matriz_entrada_back_exchange.png"

    matriz_path = baixar_arquivo_drive(matriz_nome_drive, PASTA_ENTRADA_ID, matriz_nome_local)

    if matriz_path:
        logger.info(f"Arquivo {matriz_nome_drive} baixado com sucesso.")
        matriz_preenchida_path = preencher_matriz(matriz_path)

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        with open(matriz_preenchida_path, 'rb') as photo:
            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
        logger.info("Imagem enviada ao Telegram com sucesso.")
    else:
        logger.error(f"Arquivo {matriz_nome_drive} não encontrado na pasta do Drive.")

if __name__ == "__main__":
    asyncio.run(main())

