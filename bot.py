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

# Comando /ping para teste
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot online e funcional no Railway!")

async def main():
    # Cria a aplicação com o token
    application = Application.builder().token(TOKEN).build()

    # Adiciona os handlers de comando
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))

    # Inicia o polling
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
