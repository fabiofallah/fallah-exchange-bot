import os
from flask import Flask, request
import telegram

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == '/start':
        bot.send_message(chat_id=chat_id, text='✅ Bot Fallah Exchange & Bets PRÓ está ativo e pronto!')
    elif text == '/ping':
        bot.send_message(chat_id=chat_id, text='✅ Bot online e operante no Railway!')
    else:
        bot.send_message(chat_id=chat_id, text='❌ Comando não reconhecido.')

    return 'ok'

@app.route('/')
def index():
    return '✅ Bot Fallah Exchange & Bets PRÓ online.'

if __name__ == '__main__':
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host=
