import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuração de logging para rastrear atividades no Railway
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Lê o token de ambiente corretamente
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
if not telegram_bot_token:
    logger.error("TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente.")
    exit(1)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Robô Fallah Exchange PRO ativo e pronto para operar!")

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envie /start para confirmar que o bot está online e pronto.")

# Função principal de inicialização do bot
async def main():
    application = Application.builder().token(telegram_bot_token).build()

    # Adiciona comandos ao bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Inicia o bot em polling
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
