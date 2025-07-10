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

    # Dados reais de exemplo
    estadio = "MetLife Stadium"
    competicao = "FIFA Club WC"
    odds = "2.44"
    stake = "R$ 100"
    mercado = "Match Odds"
    liquidez = "450K"
    horario = "16:00"
    resultado = "Aguardando"

    # Lista dos dados
    dados = [estadio, competicao, odds, stake, mercado, liquidez, horario, resultado]
    # Posições verticais alinhadas com os emojis
    y_positions = [540, 625, 710, 795, 880, 965, 1050, 1135]
    x_coluna = 380  # alinhamento horizontal consistente

    for idx, dado in enumerate(dados):
        posicao = (x_coluna, y_positions[idx])
        logger.info(f"Escrevendo '{dado}' em {posicao}")
        cv2.putText(
            img,
            dado,
            posicao,
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
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
    logger.info("Iniciando envio automático da matriz de ENTRADA refinada, sem texto extra no topo...")

    matriz_nome_drive = "Matriz Entrada Back Exchange.png"
    matriz_nome_local = "matriz_entrada_back_exchange.png"

    matriz_path = baixar_arquivo_drive(matriz_nome_drive, PASTA_ENTRADA_ID, matriz_nome_local)

    if matriz_path:
        logger.info(f"Arquivo {matriz_nome_drive} baixado com sucesso.")
        matriz_preenchida_path = preencher_matriz(matriz_path)

        if os.path.exists(matriz_preenchida_path):
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            logger.info(f"Enviando a imagem gerada: {matriz_preenchida_path}")
            with open(matriz_preenchida_path, 'rb') as photo:
                await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
            logger.info("Imagem enviada ao Telegram com sucesso.")
        else:
            logger.error(f"Arquivo gerado {matriz_preenchida_path} não encontrado. Envio abortado.")
    else:
        logger.error(f"Arquivo {matriz_nome_drive} não encontrado na pasta do Drive.")

if __name__ == "__main__":
    asyncio.run(main())
