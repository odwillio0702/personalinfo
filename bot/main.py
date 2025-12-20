import json
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, send_from_directory
import threading
import os

from bot.config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL

# ==============================
# БОТ
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(
            "Открыть профиль",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(
        message.chat.id,
        "клац👇",
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        print("WEBAPP DATA:", data)

        text = (
            f"👤 Открытие профиля\n\n"
            f"ID: {data.get('id')}\n"
            f"Имя: {data.get('first_name','')}\n"
            f"Username: @{data.get('username','')}\n"
            f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )

        bot.send_message(CHANNEL_ID, text)
    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# FLASK ДЛЯ САЙТА
# ==============================
app = Flask(__name__, static_folder="docs")  # папка docs вместо web

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# ==============================
# Функция запуска Flask
# ==============================
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ==============================
# ЗАПУСК БОТА И САЙТА
# ==============================
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # запускаем сайт в отдельном потоке
    print("Bot started")
    bot.infinity_polling()