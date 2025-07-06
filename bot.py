from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
import asyncio
import os

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Configuração da aplicação do bot
application = Application.builder().token(TOKEN).build()

# Comando /start
async def start(update, context):
    await update.message.reply_text("✅ Robô Fallah Exchange & Bets PRO está online e funcionando!")

application.add_handler(CommandHandler("start", start))

# Rota do webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

# Rota de verificação
@app.route("/", methods=["GET"])
def index():
    return "✅ Robô Fallah Exchange & Bets PRO ativo!", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=PORT)

