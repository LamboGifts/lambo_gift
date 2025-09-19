import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username

    data = load_data()
    if user_id not in data:
        data[user_id] = {"balance": 1000}
        save_data(data)

    keyboard = [
        [InlineKeyboardButton("🎮 Играть", web_app=WebAppInfo(url="https://your-domain.com"))],
        [InlineKeyboardButton("💳 Баланс", callback_data="balance")],
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {username or user_id}! 👋\nВыбери действие:",
        reply_markup=reply_markup
    )

# Баланс
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    data = load_data()

    balance = data.get(user_id, {}).get("balance", 0)
    await query.edit_message_text(f"💳 Твой баланс: {balance} монет")

# Профиль
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    username = query.from_user.username

    data = load_data()
    balance = data.get(user_id, {}).get("balance", 0)

    await query.edit_message_text(
        f"👤 Профиль:\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Баланс: {balance} монет 💰"
    )

def run_bot():
    TOKEN = "7678954168:AAG6755ngOoYcQfIt6viZKMRXRcv6dOd0vY"  # вставь сюда токен
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(balance, pattern="balance"))
    app.add_handler(CallbackQueryHandler(profile, pattern="profile"))

    app.run_polling()

if __name__ == "__main__":
    run_bot()
