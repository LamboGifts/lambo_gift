import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("7678954168:AAG6755ngOoYcQfIt6viZKMRXRcv6dOd0vY")  # укажи свой токен в переменных окружения Render
bot = Bot(token=TOKEN)

app = Flask(__name__)

# создаём диспетчер (обработчик сообщений)
dispatcher = Dispatcher(bot, None, workers=0)

# обработчик команды /start
def start(update: Update, context):
    update.message.reply_text("Привет 👋! Я живой бот на Render 🚀")

# обработчик любых сообщений
def echo(update: Update, context):
    update.message.reply_text(f"Ты написал: {update.message.text}")

# регистрируем обработчики
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# основной webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# health-check
@app.route("/")
def index():
    return "Бот жив ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
