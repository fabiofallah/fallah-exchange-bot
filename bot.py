import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Robô Fallah Exchange & Bets PRO ativo e funcionando!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! Estou online.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    # Modo webhook se desejar (descomente abaixo e ajuste o URL se quiser)
    # PORT = int(os.environ.get('PORT', 8443))
    # WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=PORT,
    #     webhook_url=f"{WEBHOOK_URL}/bot{TOKEN}"
    # )

    # Modo polling (estável para Railway enquanto não fixarmos domínio fixo SSL)
    app.run_polling()


