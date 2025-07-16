import os
import http
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext

app = Flask(__name__)

bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

# Comandos básicos
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Olá! Use /odds <código_do_esporte> para ver as odds.")

# Função /odds
def odds(update: Update, context: CallbackContext) -> None:
    import requests
    sport = context.args[0] if context.args else None
    if not sport:
        return update.message.reply_text("Use: /odds soccer_brazil_campeonato")
    params = {
        "apiKey": os.environ["ODDS_API_KEY"],
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }
    resp = requests.get(f"https://api.the-odds-api.com/v4/sports/{sport}/odds/", params=params).json()
    if not resp:
        return update.message.reply_text("Nenhum jogo encontrado.")
    g = resp[0]
    outcomes = g["bookmakers"][0]["markets"][0]["outcomes"]
    text = f"{g['home_team']} x {g['away_team']}\n" + "\n".join([f"{o['name']}: {o['price']}" for o in outcomes])
    update.message.reply_text(text)

# Adiciona handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("odds", odds))

# Rota webhook do Telegram
@app.post("/")
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "", http.HTTPStatus.NO_CONTENT

# Rota de health check (importante para Cloud Run)
@app.get("/")
def health():
    return "OK", http.HTTPStatus.OK

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)))
