import os
import telebot
import threading
import time
from storage import load, save
from keyboards import done_delay_keyboard

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("Bot token is not defined")

bot = telebot.TeleBot(BOT_TOKEN)
data = load()
temp = {}

# =======================
# Создание напоминания
# =======================
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "📝 О чём мне напоминать?")
    temp[m.chat.id] = {}
    bot.register_next_step_handler(m, get_text)

def get_text(m):
    temp[m.chat.id]["text"] = m.text
    bot.send_message(m.chat.id, "⏰ Время? (HH:MM)")
    bot.register_next_step_handler(m, get_time)

def get_time(m):
    temp[m.chat.id]["time"] = m.text
    bot.send_message(m.chat.id, "📅 Дни? (Mon,Tue,Wed)")
    bot.register_next_step_handler(m, get_days)

def get_days(m):
    uid = str(m.chat.id)
    reminder = {
        "text": temp[m.chat.id]["text"],
        "time": temp[m.chat.id]["time"],
        "days": m.text.split(","),
        "done": False,
        "delayed": False
    }
    data.setdefault(uid, []).append(reminder)
    save(data)
    bot.send_message(m.chat.id, "✅ Напоминание сохранено")

# =======================
# Callback кнопок
# =======================
@bot.callback_query_handler(func=lambda c: c.data in ["done", "delay10"])
def callback(c):
    uid = str(c.message.chat.id)
    for r in data.get(uid, []):
        if c.data == "done":
            r["done"] = True
            bot.edit_message_text(
                "🎉 Отлично! До следующего раза",
                c.message.chat.id,
                c.message.message_id
            )
        elif c.data == "delay10":
            r["delayed"] = True
            bot.edit_message_text(
                "⏰ Напоминание отложено на 10 минут",
                c.message.chat.id,
                c.message.message_id
            )
            def delayed_send():
                time.sleep(600)
                r["delayed"] = False
                if not r["done"]:
                    send(bot, c.message.chat.id, r)
            threading.Thread(target=delayed_send).start()
    save(data)

# =======================
# Функция отправки напоминания с кнопками
# =======================
def send(bot, uid, reminder):
    bot.send_message(
        uid,
        f"⏰ Напоминание:\n\n{reminder['text']}",
        reply_markup=done_delay_keyboard()  # Обязательно InlineKeyboardMarkup
    )

    def repeat():
        time.sleep(600)  # повтор через 10 минут
        if not reminder["done"] and not reminder.get("delayed", False):
            send(bot, uid, reminder)

    threading.Thread(target=repeat).start()

# =======================
# Шедулер проверяет время
# =======================
def start_scheduler():
    def loop():
        while True:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            weekday = datetime.now().strftime("%A")
            for uid, reminders in data.items():
                for r in reminders:
                    if r["time"] == now and weekday in r["days"] and not r["done"]:
                        send(bot, int(uid), r)
            time.sleep(60)
    threading.Thread(target=loop, daemon=True).start()

start_scheduler()

print("Бот запущен с кнопками")
bot.infinity_polling()