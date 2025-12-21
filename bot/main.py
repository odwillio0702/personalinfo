import os
import json
from datetime import datetime
from threading import Thread

from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Импорты из пакета bot
from bot.config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL
from bot.database import init_db
from bot.handlers import register_user, send_profile  # Только импорт функций

# ==============================
# Инициализация базы данных
# ==============================
init_db()  # создаем таблицу если нет

# ==============================
# Создаем бота
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# /start
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(
            "Открыть профиль",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(message.chat.id, "клац👇", reply_markup=markup)

# ==============================
# Данные с WebApp
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

        # Здесь можно добавить обработку лайков/счетчиков через register_user/send_profile
        register_user(data)

    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# Flask
# ==============================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# ==============================
# Запуск бота и Flask одновременно
# ==============================
if __name__ == "__main__":
    print("Bot started")
    Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))