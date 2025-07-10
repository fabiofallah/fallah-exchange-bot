import os
import logging
import asyncio
from telegram import Bot
from utils_drive import baixar_arquivo_drive
import cv2

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PASTA_ENTRADA_ID = os.environ['PASTA_ENTRADA_ID']

# Função para preencher a matriz usando OpenCV
def preencher_matriz(matriz_path):
    logger.info(f"Abrindo matriz com OpenCV: {matriz_path}")
    img = cv2.imread(matriz_path)

    estadio = "MetLife Stadium"
    competicao = "FIFA Club WC"
    odds = "2.44"
    stake = "R$ 100"
    mercado = "Match Odds"
    liquidez = "450K"
    horario = "16:00"
    resultado = "Aguardando"

    # Texto no topo (branco)
    cv2.putText(img, "BACK - LAY", (25
