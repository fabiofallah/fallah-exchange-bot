# ✅ Versão completa e corrigida para `fallah_drive_send_bot.py`, alinhada com seu projeto atual
# Envia para o Telegram o arquivo `Matriz Entrada Back Exchange.png` corretamente sem erro

import os
import logging
from telegram import Bot
from utils_drive import baixar_arquivo_drive

# Configurações de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar o bot do Telegram
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def main():
    try:
        logging.info("📥 Iniciando download da matriz do Drive...")
        nome_arquivo = 'Matriz Entrada Back Exchange.png'
        destino = 'matrizes_oficiais/Matriz Entrada Back Exchange.png'

        arquivo_baixado = baixar_arquivo_drive(nome_arquivo, 'entrada', destino)

        if not arquivo_baixado:
            logging.error(f"❌ Falha ao baixar {nome_arquivo} do Drive.")
            return

        logging.info("⚡ Gerando imagem com dados e escudo...")
        from gerar_imagem_matriz import gerar_imagem_matriz
        gerar_imagem_matriz()  # executa a função diretamente para gerar a imagem atualizada

        # Alinhar com o arquivo gerado corretamente:
        image_path = 'matrizes_oficiais/Matriz Entrada Back Exchange.png'

        if not os.path.exists(image_path):
            logging.error(f"❌ Imagem {image_path} não encontrada para envio.")
            return

        logging.info("📤 Enviando imagem ao Telegram...")
        with open(image_path, 'rb') as img:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)
        logging.info("✅ Imagem enviada ao Telegram com sucesso.")

    except Exception as e:
        logging.error(f"Erro no envio ao Telegram: {e}")

if __name__ == '__main__':
    main()
