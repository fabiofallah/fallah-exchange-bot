import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=4, use_context=True)

# Comandos

def start(update: Update, context):
    update.message.reply_text('✅ Bot Fallah Exchange & Bets PRÓ está online e pronto para enviar suas entradas!')

def ping(update: Update, context):
    update.message.reply_text('✅ Pong! Bot online e operacional.')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('ping', ping))

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    # Configuração do webhook automático no Railway
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
