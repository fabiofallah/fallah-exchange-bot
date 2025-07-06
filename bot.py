from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, ApplicationBuilder
import asyncio
import os

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Função de comando /start
async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Robô Fallah Exchange & Bets PRO online e funcionando!")

# Configuração do webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "✅ Robô Fallah Exchange & Bets PRO ativo!", 200

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    PORT = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=PORT)

