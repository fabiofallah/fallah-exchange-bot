import os
import logging
from telegram import Bot
from utils_drive import baixar_arquivo_drive

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Variáveis de ambiente do Railway
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def main():
    try:
        matriz_nome_drive = 'Matriz Entrada Back Exchange.png'
        tipo_operacao = 'ENTRADA'
        caminho_matriz = 'matrizes_oficiais'

        # Baixar a matriz do Drive, se necessário
        download = baixar_arquivo_drive(matriz_nome_drive, tipo_operacao, caminho_matriz)

        if not download:
            logging.error(f"❌ Falha ao baixar {matriz_nome_drive} do Drive.")
            return

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        image_path = os.path.join(caminho_matriz, matriz_nome_drive)

        if not os.path.isfile(image_path):
            logging.error(f"❌ Arquivo {image_path} não encontrado para envio.")
            return

        with open(image_path, 'rb') as img:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)
            logging.info(f"✅ Imagem '{matriz_nome_drive}' enviada com sucesso ao Telegram.")

    except Exception as e:
        logging.error(f"❌ Erro no envio de imagem: {e}")

if __name__ == '__main__':
    main()
