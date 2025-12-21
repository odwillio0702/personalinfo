import os
import json
from datetime import datetime
from threading import Thread

from flask import Flask
import telebot

# ==============================
# Абсолютные импорты из bot
# ==============================
from bot.config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL
from bot.database import init_db
from bot.handlers import register_user, send_profile

# ==============================
# Создаём Flask
# ==============================
app = Flask(__name__)

# ==============================
# Инициализация базы данных
# ==============================
init_db()  # создаём таблицы, если их нет

# ==============================
# Создаём бота
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# /start
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton(
            "Открыть профиль",
            web_app=telebot.types.WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(message.chat.id, "клац👇", reply_markup=markup)

# ==============================
# Обработка данных с WebApp
# ==============================
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

        # Можно тут вызывать функции из handlers.py, например:
        # register_user(data)
        # send_profile(data)

    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# Flask маршрут
# ==============================
@app.route("/")
def home():
    return "Bot is running!"

# ==============================
# Запуск Flask и бота одновременно
# ==============================
if __name__ == "__main__":
    print("Bot started")
    Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))