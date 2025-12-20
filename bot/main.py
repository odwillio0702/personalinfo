import os
import json
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv

# ==============================
# ЗАГРУЗКА ПЕРЕМЕННЫХ ИЗ .ENV
# ==============================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Приватный канал, например -1001234567890
WEBAPP_URL = "https://odwillio0702.github.io/personalinfo/"  # Ссылка на WebApp

# ==============================
# СОЗДАЁМ БОТА
# ==============================
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================
# КНОПКА ДЛЯ ОТКРЫТИЯ WEBAPP
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
    bot.send_message(message.chat.id, "👇", reply_markup=markup)

# ==============================
# ОБРАБОТКА ДАННЫХ С WEBAPP
# ==============================
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    try:
        data = json.loads(message.web_app_data.data)
        print("Received data:", data)  # Проверка в консоли

        if data.get("action") == "log_user":
            text = (
                f"👤 Пользователь открыл WebApp\n"
                f"ID: {data.get('id')}\n"
                f"Имя: {data.get('first_name')} {data.get('last_name','')}\n"
                f"Username: @{data.get('username','')}\n"
                f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            bot.send_message(CHANNEL_ID, text)

    except Exception as e:
        print("Ошибка при обработке данных:", e)

# ==============================
# ЗАПУСК БОТА
# ==============================
bot.infinity_polling()