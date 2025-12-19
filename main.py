import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# -------------------------------
# ВАШИ ТОКЕНЫ
BOT_TOKEN = "ВАШ_BOT_TOKEN"
# -------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

# -------------------------------
# КОМАНДА /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    # Кнопка открытия WebApp
    markup.add(
        KeyboardButton(
            "👤 Открыть профиль",
            web_app=WebAppInfo(
                url="https://odwillio0702.github.io/telegram-schedulebot/"
            )
        )
    )

    bot.send_message(
        message.chat.id,
        "👇",
        reply_markup=markup
    )

# -------------------------------
# Пример простой команды
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Список команд:\n/start — открыть профиль\n/help — показать это сообщение"
    )

# -------------------------------
# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()