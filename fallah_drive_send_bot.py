import os
import logging
from telegram import Bot
from utils_drive import baixar_arquivo_drive

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def main():
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        matriz_nome_drive = 'Matriz Entrada Back Exchange.png'
        tipo_operacao = 'ENTRADA'
        caminho_matriz = os.path.join('matrizes_oficiais', matriz_nome_drive)

        caminho_baixado = baixar_arquivo_drive(matriz_nome_drive, tipo_operacao, caminho_matriz)

        if caminho_baixado:
            with open(caminho_baixado, 'rb') as img:
                bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)
            logging.info(f"✅ Imagem '{matriz_nome_drive}' enviada com sucesso ao Telegram.")
        else:
            logging.error("❌ Falha ao baixar ou encontrar a matriz para envio.")

    except Exception as e:
        logging.error(f"❌ Erro ao enviar imagem ao Telegram: {e}")

if __name__ == '__main__':
    main()
