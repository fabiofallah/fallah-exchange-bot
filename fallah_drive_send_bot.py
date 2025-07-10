import os
import json
import logging
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont

# Configurações iniciais
logging.basicConfig(level=logging.INFO)
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Função para preencher a matriz de entrada com escudos e dados
def preencher_matriz(matriz_path):
    imagem = Image.open(matriz_path).convert('RGB')
    draw = ImageDraw.Draw(imagem)
    
    # Carregar fonte
    font = ImageFont.load_default()

    # Inserir textos (dados reais do jogo solicitado)
    draw.text((90, 360), "MetLife Stadium", fill="black", font=font)
    draw.text((90, 390), "FIFA Club World Cup", fill="black", font=font)
    draw.text((90, 420), "2.44", fill="black", font=font)
    draw.text((90, 450), "100", fill="black", font=font)
    draw.text((90, 480), "Back PSG", fill="black", font=font)
    draw.text((90, 510), "450K", fill="black", font=font)
    draw.text((90, 540), "16:00", fill="black", font=font)
    draw.text((90, 570), "-", fill="black", font=font)

    # Inserir escudos se desejado futuramente (completaremos depois)

    output_path = "matriz_entrada_preenchida.png"
    imagem.save(output_path)
    return output_path

# Função principal
async def main():
    logging.info("Iniciando envio automático da matriz de ENTRADA...")
    matriz_path = "matriz_entrada.png"  # Nome padrão usado no download

    if not os.path.exists(matriz_path):
        logging.error("Arquivo matriz_entrada.png não encontrado.")
        return

    matriz_preenchida_path = preencher_matriz(matriz_path)
    with open(matriz_preenchida_path, 'rb') as photo:
        await bot.send_photo(chat_id=CHAT_ID, photo=photo)
        logging.info("Imagem enviada ao Telegram com sucesso.")

if __name__ == "__main__":
    asyncio.run(main())
