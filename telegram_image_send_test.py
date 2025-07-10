# telegram_image_send_test.py

import asyncio
from telegram import Bot
import os

async def send_image():
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Confirme que o caminho abaixo está correto e aponta para o arquivo PNG
    image_path = 'matriz_teste_envio.png'

    try:
        with open(image_path, 'rb') as img:
            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img, caption="Envio de teste do Robô Fallah Exchange PRO.")
        print("✅ Imagem enviada com sucesso para o Telegram.")
    except Exception as e:
        print(f"❌ Erro ao enviar imagem: {e}")

if __name__ == '__main__':
    asyncio.run(send_image())
