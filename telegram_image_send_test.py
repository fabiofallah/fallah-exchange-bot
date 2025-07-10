import os
import asyncio
from telegram import Bot

async def enviar_imagem_telegram():
    try:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not token or not chat_id:
            print("❌ TOKEN ou CHAT_ID não configurados nas variáveis de ambiente.")
            return

        bot = Bot(token=token)

        caminho_imagem = 'app/matrizes_oficiais/Matriz Entrada Back Exchange.png'

        if not os.path.isfile(caminho_imagem):
            print(f"❌ Arquivo não encontrado: {caminho_imagem}")
            return

        with open(caminho_imagem, 'rb') as img:
            await bot.send_photo(chat_id=chat_id, photo=img)

        print(f"✅ Imagem '{caminho_imagem}' enviada com sucesso ao Telegram.")

    except Exception as e:
        print(f"❌ Erro ao enviar imagem ao Telegram: {e}")

if __name__ == "__main__":
    asyncio.run(enviar_imagem_telegram())
