import telebot
from telebot import types

BOT_TOKEN = "8485092572:AAHIdjrrXBOaIPD6-wN17cXtxleHYOWxJiw"
bot = telebot.TeleBot(BOT_TOKEN)

# ================== Команды ==================
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    # Кнопка для открытия Mini App
    web_app = types.WebAppInfo(url="web_app=WebAppInfo(
    url="https://brilliant-licorice-c5ff84.netlify.app"
)")
    button = types.InlineKeyboardButton(text="Открыть приложение", web_app=web_app)
    keyboard.add(button)
    
    bot.send_message(message.chat.id, "!?/$%??!", reply_markup=keyboard)

# ================== Старт бота ==================
bot.infinity_polling()
