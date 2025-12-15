import os
import telebot
import threading
import time
from datetime import datetime

# -----------------------
# Настройки
# -----------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("Bot token is not defined")

bot = telebot.TeleBot(BOT_TOKEN)
data_file = "data.json"

try:
    import json
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            json.dump({}, f)
except:
    pass

# -----------------------
# Хранилище
# -----------------------
def load_data():
    with open(data_file, "r") as f:
        return json.load(f)

def save_data(d):
    with open(data_file, "w") as f:
        json.dump(d, f)

data = load_data()
temp = {}

# -----------------------
# Создание напоминания
# -----------------------
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "📝 О чём напоминать?")
    temp[m.chat.id] = {}
    bot.register_next_step_handler(m, get_text)

def get_text(m):
    temp[m.chat.id]["text"] = m.text
    bot.send_message(m.chat.id, "⏰ Время (HH:MM, 24h)? Например 14:30")
    bot.register_next_step_handler(m, get_time)

def get_time(m):
    text = m.text.strip()
    try:
        h, minute = map(int, text.split(":"))
        if not (0 <= h < 24 and 0 <= minute < 60):
            raise ValueError
        temp[m.chat.id]["time"] = f"{h:02d}:{minute:02d}"
        bot.send_message(
            m.chat.id,
            "📅 Дни (Mon,Tue,Wed,Thu,Fri,Sat,Sun) через запятую.\n"
            "Пример: Mon,Wed,Fri"
        )
        bot.register_next_step_handler(m, get_days)
    except:
        bot.send_message(m.chat.id, "❌ Неверный формат времени! Попробуй ещё раз (HH:MM)")
        bot.register_next_step_handler(m, get_time)

def get_days(m):
    valid_days = {"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}
    days = [d.strip() for d in m.text.split(",")]
    if not all(d in valid_days for d in days):
        bot.send_message(m.chat.id, "❌ Ошибка! Дни должны быть через запятую, пример: Mon,Wed,Fri")
        bot.register_next_step_handler(m, get_days)
        return
    uid = str(m.chat.id)
    reminder = {
        "text": temp[m.chat.id]["text"],
        "time": temp[m.chat.id]["time"],
        "days": days,
        "done": False,
        "delayed": False
    }
    data.setdefault(uid, []).append(reminder)
    save_data(data)
    bot.send_message(m.chat.id, "✅ Напоминание сохранено с кнопками")

# -----------------------
# Кнопки
# -----------------------
def create_buttons():
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton("✅ Я сделал", callback_data="done"))
    kb.add(telebot.types.InlineKeyboardButton("⏰ Отложить 10 мин", callback_data="delay10"))
    return kb

# -----------------------
# Callback кнопок
# -----------------------
@bot.callback_query_handler(func=lambda c: c.data in ["done", "delay10"])
def callback(c):
    uid = str(c.message.chat.id)
    for r in data.get(uid, []):
        if c.data == "done":
            r["done"] = True
            bot.edit_message_text("🎉 Отлично! До следующего раза", c.message.chat.id, c.message.message_id)
        elif c.data == "delay10":
            r["delayed"] = True
            bot.edit_message_text("⏰ Напоминание отложено на 10 минут", c.message.chat.id, c.message.message_id)
            def delayed_send():
                time.sleep(600)
                r["delayed"] = False
                if not r["done"]:
                    send_reminder(c.message.chat.id, r)
            threading.Thread(target=delayed_send).start()
    save_data(data)

# -----------------------
# Отправка напоминания
# -----------------------
def send_reminder(uid, reminder):
    bot.send_message(uid, f"⏰ Напоминание:\n\n{reminder['text']}", reply_markup=create_buttons())
    def repeat():
        time.sleep(600)
        if not reminder["done"] and not reminder.get("delayed", False):
            send_reminder(uid, reminder)
    threading.Thread(target=repeat).start()

# -----------------------
# Шедулер
# -----------------------
def start_scheduler():
    def loop():
        while True:
            now = datetime.now()
            weekday_full = now.strftime("%A")
            weekday_map = {
                "Monday":"Mon","Tuesday":"Tue","Wednesday":"Wed",
                "Thursday":"Thu","Friday":"Fri","Saturday":"Sat","Sunday":"Sun"
            }
            today = weekday_map[weekday_full]
            for uid, reminders in data.items():
                for r in reminders:
                    try:
                        h,m = map(int,r["time"].split(":"))
                        reminder_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
                    except:
                        continue
                    if now >= reminder_time and today in r["days"] and not r["done"] and not r.get("delayed", False):
                        send_reminder(int(uid), r)
            time.sleep(10)
    threading.Thread(target=loop, daemon=True).start()

start_scheduler()
print("Бот запущен с проверкой ввода, кнопками и днями недели")
bot.infinity_polling()