import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from telegram.ext import CallbackContext

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Fallah Exchange Bot ONLINE'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Robô Fallah Exchange PRO online e configurado com sucesso.")

def ping(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Pong! O robô está online.")

from telegram.ext import Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('ping', ping))

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
