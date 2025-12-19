import telebot
from telebot import types

BOT_TOKEN = "8485092572:AAHIdjrrXBOaIPD6-wN17cXtxleHYOWxJiw"
bot = telebot.TeleBot(BOT_TOKEN)

from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(
    KeyboardButton(
        "Открыть профиль",
        web_app=WebAppInfo(
            url="https://odwillio0702.github.io/telegram-schedulebot/"
        )
    )
)

bot.send_message(chat_id, "Жми 👇", reply_markup=markup)