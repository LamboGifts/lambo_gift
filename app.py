import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# Инициализация Flask
app = Flask(__name__)

# Токен бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден! Задай переменную окружения.")

# Создаём приложение telegram-bot
application = Application.builder().token(TOKEN).build()

# Простейшая команда /start
async def start(update: Update, context):
    await update.message.reply_text("🔥 Привет! Lambo Gift Bot работает!")

# Регистрируем команду
application.add_handler(CommandHandler("start", start))


# 📌 Этот маршрут нужен Telegram для апдейтов
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok", 200

# 📌 Тестовый маршрут
@app.route("/")
def index():
    return "🔥 Lambo Gift Plinko работает! Зайди через Telegram-бота."


if __name__ == "__main__":
    # Запуск локально
    app.run(host="0.0.0.0", port=10000)
