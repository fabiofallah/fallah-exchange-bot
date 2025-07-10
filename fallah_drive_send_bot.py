import os
import logging
from telegram import Bot
import asyncio
import subprocess

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Pega variáveis do ambiente
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def main():
    try:
        # 1️⃣ Baixar a matriz do Drive
        logging.info("⏬ Iniciando download da matriz do Drive...")
        subprocess.run(['python', 'utils_drive.py'], check=True)

        # 2️⃣ Gerar a imagem com dados e escudo
        logging.info("🛠️ Gerando imagem com dados e escudo...")
        subprocess.run(['python', 'gerar_imagem_matriz.py'], check=True)

        # 3️⃣ Enviar ao Telegram a imagem gerada
        logging.info("📤 Enviando imagem ao Telegram...")
        image_path = 'matrizes_oficiais/matriz_entrada_preenchida.png'

        if not os.path.exists(image_path):
            logging.error(f"❌ Imagem {image_path} não encontrada para envio.")
            return

        with open(image_path, 'rb') as img:
            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)

        logging.info("✅ Imagem enviada ao Telegram com sucesso.")

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erro ao executar subprocesso: {e}")
    except Exception as e:
        logging.error(f"❌ Erro geral: {e}")

if __name__ == '__main__':
    asyncio.run(main())
