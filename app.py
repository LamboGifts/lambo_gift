from flask import Flask, render_template, request, jsonify
import json
import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

# ====== Настройки ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7678954168:AAG6755ngOoYcQfIt6viZKMRXRcv6dOd0vY")
bot = Bot(token=TELEGRAM_TOKEN)

# ====== Главная страница (Plinko) ======
@app.route("/")
def index():
    return "🔥 Lambo Gift Plinko работает! Зайди через Telegram-бота."

# ====== Страница игры с user_id ======
@app.route("/game/<user_id>")
def game(user_id):
    return render_template("index.html", user_id=user_id)

# ====== API для сохранения результатов ======
@app.route("/save_result", methods=["POST"])
def save_result():
    data = request.json
    user_id = str(data.get("user_id"))
    score = data.get("score")

    if not user_id or score is None:
        return jsonify({"status": "error", "message": "Нет user_id или score"}), 400

    # Загружаем старые данные
    file_path = "data.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    else:
        results = {}

    # Сохраняем результат
    results[user_id] = score

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "ok", "user_id": user_id, "score": score})

# ====== Команда /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    url = f"https://ТВОЙ_САЙТ.onrender.com/game/{user_id}"

    keyboard = [[InlineKeyboardButton("🎮 Играть в Plinko", web_app={"url": url})]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 🚀\n"
        "Добро пожаловать в *Lambo Gift Plinko*.\n"
        "Нажми кнопку ниже, чтобы начать игру 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ====== Запуск телеграм-бота ======
def run_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
