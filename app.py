import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# токен бота из Render Environment (чтобы не палить его в коде)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# создаем Flask
app = Flask(__name__)

# создаем Telegram Application
application = Application.builder().token(TOKEN).build()

# команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Бот работает через webhook 🚀")

application.add_handler(CommandHandler("start", start))

# Flask route для webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

# healthcheck
@app.route("/")
def home():
    return "Бот жив ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
