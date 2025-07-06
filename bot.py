import os
import time
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configuração de log simples
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Pega o token do Railway (variável TELEGRAM_BOT_TOKEN já configurada)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

# Comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Olá, você está conectado ao Fallah Exchange & Bets PRÓ 🚀. Aguarde as entradas automáticas aqui.")

# Comando de teste
def ping(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot está online e funcional no Railway!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            logging.error(f"Erro no bot: {e}")
            time.sleep(5)  # espera 5 segundos antes de reiniciar em caso de erro
