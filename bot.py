import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler

# Variáveis de ambiente
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# Comandos
async def start(update: Update, context):
    await update.message.reply_text("✅ Bot Fallah Exchange & Bets PRÓ está online e pronto!")

async def ping(update: Update, context):
    await update.message.reply_text("✅ Pong! Bot ativo no Railway.")

# Adiciona handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("ping", ping))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put_nowait(update)
    return "ok", 200

@app.route("/", methods=["GET"])
async def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    await bot_app.bot.set_webhook(webhook_url)
    return f"✅ Webhook configurado em {webhook_url}", 200

if __name__ == "__main__":
    bot_app.run_webhook(listen="0.0.0.0",
                        port=int(os.environ.get("PORT", 5000)),
                        webhook_url=f"{WEBHOOK_URL}/{TOKEN}")



