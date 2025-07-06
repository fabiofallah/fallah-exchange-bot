import os
import logging
import asyncio
import nest_asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ajuste para evitar conflito de loop no Railway
nest_asyncio.apply()

# Configuração de log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logging.error("❌ TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente.")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Robô Fallah Exchange PRO está ativo e funcionando no Railway!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot está online e respondendo corretamente!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

