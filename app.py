import os
from flask import Flask, request
import telegram

# Токен бота берём из переменных окружения (Render → Settings → Environment)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def index():
    return "Бот жив ✅"

# Webhook обработчик
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        if text == "/start":
            bot.sendMessage(chat_id=chat_id, text="Привет 👋! Я жив и работаю на Render 🚀")
        else:
            bot.sendMessage(chat_id=chat_id, text=f"Ты написал: {text}")

    return "ok"
