import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuração de log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Pega o token do Railway
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Verificação se o token existe
if not TOKEN:
    logging.error("❌ TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente.")
    exit(1)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Fallah Exchange & Bets PRÓ está ativo e pronto para receber suas entradas!")

# Comando /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot online e funcional no Railway!")

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
