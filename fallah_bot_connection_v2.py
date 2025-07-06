# Fallah Exchange & Bets PRO - Monitor de Conexão Telegram (VERSÃO CORRIGIDA COM user_list)

import time
import os
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

# CONFIGURAÇÕES
your_telegram_bot_token = "7777458509:AAHfshLsxT0dyN30NeY_6zTOnUfQMWJNo58"
connected_image_path = "Alerta de Conexão Telegram.png"
disconnected_image_path = "Alerta de Desconexão Telegram.png"

bot = Bot(token=your_telegram_bot_token)
application = Application.builder().token(your_telegram_bot_token).build()
dispatcher = updater.dispatcher

is_connected = True
users_file = "users.txt"

def save_user(chat_id):
    with open(users_file, "a") as f:
        f.write(str(chat_id) + "\n")

def get_users():
    if not os.path.exists(users_file):
        return []
    with open(users_file, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        # Salva o usuário no arquivo se ainda não existir
        current_users = get_users()
        if str(chat_id) not in current_users:
            save_user(chat_id)
        
        context.bot.send_photo(
            chat_id=chat_id,
            photo=open(connected_image_path, "rb"),
            caption="✅ Conexão Estabelecida\nSeu robô está ativo e pronto para enviar operações."
        )
        print(f"Imagem de conexão enviada para {chat_id}")
    except Exception as e:
        print(f"Erro ao enviar imagem de conexão: {e}")

def monitor():
    global is_connected
    while True:
        try:
            print("Verificando conexão...")
            # Simulação: aqui você coloca sua checagem real do robô (ping, operação, etc.)
            # Se tudo certo, mantém conectado
            is_connected = True
        except Exception as e:
            print(f"Erro detectado: {e}")
            if is_connected:
                try:
                    users = get_users()
                    for user in users:
                        bot.send_photo(
                            chat_id=user,
                            photo=open(disconnected_image_path, "rb"),
                            caption="🚨 Alerta de Desconexão\nSeu robô pode ter parado de funcionar, verifique sua conexão."
                        )
                        print(f"Imagem de desconexão enviada para {user}")
                except Exception as e:
                    print(f"Erro ao enviar alerta de desconexão: {e}")
                is_connected = False
        time.sleep(30)  # Intervalo de checagem de 30 segundos

def main():
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    print("Robô de monitoramento iniciado e aguardando comandos...")

    monitor()

if __name__ == "__main__":
    main()
