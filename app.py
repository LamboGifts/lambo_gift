from flask import Flask, request
from telegram import Update
from telegram.ext import Application

TOKEN = "7678954168:AAG6755ngOoYcQfIt6viZKMRXRcv6dOd0vY"

app = Flask(__name__)

# создаём Application (асинхронный бот)
application = Application.builder().token(TOKEN).build()


# команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Бот работает ✅")


application.add_handler(
    __import__("telegram.ext").CommandHandler("start", start)
)


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put_nowait(update)  # асинхронно
    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "🔥 Webhook бот работает!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
