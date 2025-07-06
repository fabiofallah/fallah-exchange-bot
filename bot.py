import os
import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configuração de log simples
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Pega o token do Railway de forma segura
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Verificação de token para debug
if not TOKEN:
    logging.error("🚨 TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente.")
    exit(1)

# Instancia o bot
bot = Bot(token=TOKEN)

# Comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot Fallah Exchange & Bets PRÓ está ativo e pronto para enviar suas entradas!")

# Comando /ping para teste
def ping(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot está online no Railway!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
