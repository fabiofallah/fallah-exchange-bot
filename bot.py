from flask import Flask
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

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

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))
    application.run_polling()

