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

    # Dados
    estadio = "MetLife Stadium"
    competicao = "FIFA Club WC"
    odds = "2.44"
    stake = "R$ 100"
    mercado = "Match Odds"
    liquidez = "450K"
    horario = "16:00"
    resultado = "Aguardando"

    # Escrita na parte de cima (área escura) - se quiser manter
    cv2.putText(img, "BACK - LAY", (250, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3, cv2.LINE_AA)

    # Escrita dentro do quadro bege (cor preta)
    dados = [estadio, competicao, odds, stake, mercado, liquidez, horario, resultado]
    y_inicial = 480
    y_salto = 82

    for idx, dado in enumerate(dados):
        posicao = (380, y_inicial + idx * y_salto)
        logger.info(f"Escrevendo '{dado}' em {posicao}")
        cv2.putText(
            img,
            dado,
            posicao,
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 0, 0),
            3,
            cv2.LINE_AA
        )

    output_path = os.path.join(os.getcwd(), "matriz_entrada_preenchida.png")
    cv2.imwrite(output_path, img)
    logger.info(f"Imagem gerada e salva em: {output_path}")

    return output_path

# Função principal
async def main():
    logger.info("Iniciando envio automático da matriz de ENTRADA com alinhamento corrigido...")

    matriz_nome_drive = "Matriz Entrada Back Exchange.png"
    matriz_nome_local = "matriz_entrada_back_exchange.png"

    matriz_path = baixar_arquivo_drive(matriz_nome_drive, PASTA_ENTRADA_ID, matriz_nome_local)
