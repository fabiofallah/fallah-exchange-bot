import os
import logging
import asyncio
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
    img = Image.open(matriz_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    try:
        fonte = ImageFont.truetype("arial.ttf", 42)  # Tamanho ideal para a matriz
    except:
        fonte = ImageFont.load_default()
        logger.warning("Fonte arial.ttf não encontrada. Usando fonte padrão.")

    # Dados fixos
    estadio = "MetLife Stadium"
    competicao = "FIFA Club World Cup"
    odds = "2.44"
    stake = "R$ 100"
    mercado = "Match Odds"
    liquidez = "450K"
    horario = "16:00"
    resultado = "Aguardando"

    # Coordenadas alinhadas no bloco bege (ajustadas pela matriz recebida)
    x_coluna = 300
    y_inicial = 435
    y_salto = 85

    draw.text((x_coluna, y_inicial + 0 * y_salto), f"{estadio}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 1 * y_salto), f"{competicao}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 2 * y_salto), f"{odds}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 3 * y_salto), f"{stake}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 4 * y_salto), f"{mercado}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 5 * y_salto), f"{liquidez}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 6 * y_salto), f"{horario}", font=fonte, fill="black")
    draw.text((x_coluna, y_inicial + 7 * y_salto), f"{resultado}", font=fonte, fill="black")

    output_path_

