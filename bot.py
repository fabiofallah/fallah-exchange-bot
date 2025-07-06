import os
import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Obtém o token do Railway (variável de ambiente)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Fallah Exchange PRÓ está ativo e pronto para enviar entradas!")

# Comando /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot está online no Railway!")

# Inicialização principal
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))

    # Aplicar nest_asyncio para evitar erros de loop no Railway
    nest_asyncio.apply()

    # Rodar o bot
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
