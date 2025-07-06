import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Função de resposta ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Fallah Exchange Bot ativo e funcionando!')

# Função principal
async def main():
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if telegram_token is None:
        print("Erro: TELEGRAM_BOT_TOKEN não encontrado nas variáveis de ambiente.")
        return

    application = Application.builder().token(telegram_token).build()

    # Adiciona o handler para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o bot
    await application.run_polling()

# Executa o bot corretamente ao iniciar
if __name__ == '__main__':
    asyncio.run(main())
