import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=4, use_context=True)

def start(update: Update, context):
    update.message.reply_text('🤖 Robô Fallah Exchange PRÓ está online e funcionando via Railway webhook.')

def ping(update: Update, context):
    update.message.reply_text('✅ Pong: Robô ativo.')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('ping', ping))

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

if __name__ == '__main__':
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
