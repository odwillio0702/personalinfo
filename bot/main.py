import json
import os
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv

# ==============================
# ЗАГРУЗКА ПЕРЕМЕННЫХ
# ==============================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
WEBAPP_URL = os.getenv("WEBAPP_URL")

if not BOT_TOKEN or CHANNEL_ID == 0 or not WEBAPP_URL:
    raise ValueError("❌ BOT_TOKEN, CHANNEL_ID или WEBAPP_URL не определены в переменных окружения!")

# ==============================
# СОЗДАЁМ БОТА
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
    bot.send_message(
        message.chat.id,
        "клац👇",
        reply_markup=markup
    )

# ==============================
# ОБРАБОТКА ДАННЫХ С WEBAPP
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

    except Exception as e:
        print("Ошибка WebApp:", e)

# ==============================
# ЗАПУСК
# ==============================
if __name__ == "__main__":
    print("Bot started")
    bot.infinity_polling()