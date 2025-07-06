import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Comandos de teste
def start(update: Update, context):
    update.message.reply_text("✅ Bot Fallah Exchange & Bets PRÓ está online e pronto para enviar suas entradas!")

def ping(update: Update, context):
    update.message.reply_text("✅ Pong! Bot ativo no Railway.")

# Configura dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("ping", ping))

# Endpoint do webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok', 200

# Inicializa webhook
@app.route('/')
def set_webhook():
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    return f"Webhook configurado para {WEBHOOK_URL}/{TOKEN}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

