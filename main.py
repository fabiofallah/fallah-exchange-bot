from flask import Flask, request
import telegram
import os

TOKEN = '7777458509:AAHfshLsxT0dyN30NeY_6zTOnUfQMWJNo58'
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# Mensagem de boas-vindas
WELCOME_MESSAGE = (
    "Olá, seja bem-vindo ao Fallah Exchange & Bets PRO!\n"
    "Sou o Robô Fallah e vou te acompanhar em todas as operações."
)

# Flags de controle
user_started = set()  # Guarda quem já recebeu a saudação
engine_status = {"connected": True}  # Estado atual

# Caminhos fixos do Drive montado ou sincronizado localmente
IMG_CONECTADO = '/telegram/Matriz Conexão.png'
IMG_DESCONECTADO = '/telegram/Matriz Desconexão.png'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            if chat_id not in user_started:
                bot.send_message(chat_id=chat_id, text=WELCOME_MESSAGE)
                user_started.add(chat_id)
    
    return "ok"

# 🔄 Funções chamadas externamente por comandos para status de conexão
def engine_connect():
    if not engine_status["connected"]:
        for chat_id in user_started:
            with open(IMG_CONECTADO, 'rb') as img:
                bot.send_photo(chat_id=chat_id, photo=img)
        engine_status["connected"] = True

def engine_disconnect():
    if engine_status["connected"]:
        for chat_id in user_started:
            with open(IMG_DESCONECTADO, 'rb') as img:
                bot.send_photo(chat_id=chat_id, photo=img)
        engine_status["connected"] = False

if __name__ == "__main__":
    app.run(port=8080)
