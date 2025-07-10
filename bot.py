from flask import Flask
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import subprocess

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN)

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Robô Fallah Exchange PRÓ ativo e online.")

@app.route('/')
def home():
    return 'Bot Fallah Exchange PRÓ rodando com sucesso!'

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('pong')

async def gerar_entrada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Gerando entrada, aguarde...")

    try:
        subprocess.run(['python', 'fallah_drive_send_bot.py'], check=True)
        subprocess.run(['python', 'gerar_imagem_matriz.py'], check=True)

        chat_id = update.effective_chat.id
        bot.send_photo(chat_id=chat_id, photo=open('matriz_entrada_preenchida.png', 'rb'))

        await update.message.reply_text("✅ Imagem gerada e enviada com sucesso.")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ Erro ao gerar ou enviar a imagem: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))
    application.add_handler(CommandHandler('gerarentrada', gerar_entrada))
    application.run_polling()
