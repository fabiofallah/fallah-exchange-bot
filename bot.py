import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuração de log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Pega o token de forma segura
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logging.error("❌ TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente.")
    exit(1)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Fallah Exchange & Bets PRÓ está ativo e pronto para receber suas entradas!")

# Comando /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot online e funcional no Railway!")

# Main assíncrono
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
