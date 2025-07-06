import os
from flask import Flask, request
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

# Função para enviar mensagem
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Rota principal do webhook
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text == "/start":
            send_message(chat_id, "🤖 Bot Fallah Exchange & Bets PRO está online e funcionando!")
        elif text == "/ping":
            send_message(chat_id, "🏓 Pong! O bot está ativo.")
        else:
            send_message(chat_id, f"Você enviou: {text}")

    return {"ok": True}

# Início do servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
