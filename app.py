import os
from flask import Flask, request
import telegram

TOKEN = os.environ.get("TELEGRAM_TOKEN")  # в Render -> Settings -> Environment
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def index():
    return "Бот жив ✅"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.sendMessage(chat_id=chat_id, text="Привет! 🚀 Бот работает через Render")
    else:
        bot.sendMessage(chat_id=chat_id, text=f"Ты написал: {text}")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
