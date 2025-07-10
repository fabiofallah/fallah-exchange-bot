import os
import asyncio
from telegram import Bot

async def main():
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Erro: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurados no Railway.")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    image_path = 'matrizes_oficiais/Matriz Entrada Back Exchange.png'

    if not os.path.exists(image_path):
        print(f"Erro: Arquivo {image_path} não encontrado.")
        return

    with open(image_path, 'rb') as img:
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)
        print(f"✅ Imagem {image_path} enviada com sucesso ao Telegram.")

if __name__ == '__main__':
    asyncio.run(main())
