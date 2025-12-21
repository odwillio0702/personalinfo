import os
import json
from datetime import datetime
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.config import BOT_TOKEN, CHANNEL_ID, WEBAPP_URL
from bot.database import init_db
from bot.handlers import register_user, like_user

# ==============================
# Инициализация базы
# ==============================
init_db()

# ==============================
# Flask
# ==============================
app = Flask(__name__)

# ==============================
# Телеграм-бот
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Открыть профиль", web_app=WebAppInfo(url=WEBAPP_URL)))
    bot.send_message(message.chat.id, "Клац👇", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        print("WEBAPP DATA:", data)

        # Добавляем пользователя и увеличиваем просмотры
        register_user(data)

        # Отправляем сообщение в канал
        text = (
            f"👤 Открытие профиля\n\n"
            f"ID: {data.get('id')}\n"
            f"Имя: {data.get('first_name','')} {data.get('last_name','')}\n"
            f"Username: @{data.get('username','')}\n"
            f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
        bot.send_message(CHANNEL_ID, text)

    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# Flask routes
# ==============================
@app.route("/")
def home():
    return "Bot is running!"

@app.route("/like/<int:user_id>")
def like(user_id):
    like_user(user_id)
    return f"User {user_id} liked!"

# ==============================
# Запуск
# ==============================
if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))