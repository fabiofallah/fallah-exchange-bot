import os
import logging
import asyncio
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont
from utils_drive import baixar_arquivo_drive

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PASTA_ENTRADA_ID = os.environ['PASTA_ENTRADA_ID']

# Função para preencher a matriz
def preencher_matriz(matriz_path):
    logger.info(f"Abrindo matriz: {matriz_path}")
    img = Image.open(matriz_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    try:
        fonte = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        logger.info("Fonte DejaVuSans-Bold.ttf encontrada e utilizada.")
    except Exception as e:
        logger.warning(f"Fonte DejaVuSans-Bold.ttf não encontrada. Usando fonte padrão. Erro: {e}")
        fonte = ImageFont.load_default()

    estadio = "MetLife Stadium"
    competicao = "FIFA Club WC"
    odds = "2.44"
    stake = "R$ 100"
    mercado = "Match Odds"
    liquidez = "450K"
    horario = "16:00"
    resultado = "Aguardando"

    x_coluna = 300
    y_inicial = 435
    y_salto = 85

    dados = [estadio, competicao, odds, stake, mercado, liquidez, horario, resultado]

    for idx, dado in enumerate(dados):
        posicao = (x_coluna, y_inicial + idx * y_salto)
        logger.info(f"Escrevendo '{dado}' em {posicao}")
        draw.text(posicao, dado, font=fonte, fill="white")

    output_path = os.path.join(os.getcwd(), "matriz_entrada_preenchida.png")
    img.save(output_path, quality=95)
    logger.info(f"Imagem gerada e salva em: {output_path}")

    pixel = img.getpixel((310, 445))
    logger.info(f"Cor do pixel após escrita (310,445): {pixel}")

    return output_path

# Função principal
async def main():
    logger.info("Iniciando envio automático da matriz de ENTRADA...")

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
