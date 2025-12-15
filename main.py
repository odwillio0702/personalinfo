import os
import telebot
import threading
import time
from datetime import datetime, timedelta
import json

# -----------------------
# Настройки
# -----------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("Bot token is not defined")

bot = telebot.TeleBot(BOT_TOKEN)
data_file = "data.json"

# -----------------------
# Хранилище
# -----------------------
def load_data():
    if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
        with open(data_file, "w") as f:
            json.dump({}, f)
        return {}
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
    bot.send_message(
        m.chat.id,
        "✅ Напоминание сохранено!\n"
        "Команды:\n"
        "/list — показать все напоминания\n"
        "/done — отметить как выполненное\n"
        "/delay <минут> — отложить\n"
        "/delete <номер> — удалить напоминание\n"
        "/edit <номер> — изменить напоминание"
    )

# -----------------------
# Команды
# -----------------------
@bot.message_handler(commands=["list"])
def list_reminders(m):
    uid = str(m.chat.id)
    reminders = data.get(uid, [])
    if not reminders:
        bot.send_message(m.chat.id, "ℹ️ У тебя нет активных напоминаний.")
        return
    text = "📋 Твои напоминания:\n"
    for i, r in enumerate(reminders):
        status = "✅" if r["done"] else "⏰"
        text += f"{i+1}. {r['text']} ({r['time']} {','.join(r['days'])}) {status}\n"
    bot.send_message(m.chat.id, text)

@bot.message_handler(commands=["done"])
def mark_done(m):
    uid = str(m.chat.id)
    found = False
    for r in data.get(uid, []):
        if not r["done"]:
            r["done"] = True
            found = True
    save_data(data)
    msg = "🎉 Все активные напоминания отмечены как выполненные!" if found else "ℹ️ Нет активных напоминаний."
    bot.send_message(m.chat.id, msg)

@bot.message_handler(commands=["delay"])
def delay(m):
    uid = str(m.chat.id)
    args = m.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.send_message(m.chat.id, "❌ Используй: /delay <минут>")
        return
    minutes = int(args[1])
    for r in data.get(uid, []):
        if not r["done"]:
            r["delayed"] = True
            def delayed_send(rem=r, chat_id=m.chat.id):
                time.sleep(minutes*60)
                rem["delayed"] = False
                if not rem["done"]:
                    send_reminder(chat_id, rem)
            threading.Thread(target=delayed_send).start()
    bot.send_message(m.chat.id, f"⏰ Все активные напоминания отложены на {minutes} минут")
    save_data(data)

@bot.message_handler(commands=["delete"])
def delete_reminder(m):
    uid = str(m.chat.id)
    args = m.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.send_message(m.chat.id, "❌ Используй: /delete <номер>")
        return
    idx = int(args[1])-1
    reminders = data.get(uid, [])
    if 0 <= idx < len(reminders):
        removed = reminders.pop(idx)
        save_data(data)
        bot.send_message(m.chat.id, f"🗑 Напоминание удалено: {removed['text']}")
    else:
        bot.send_message(m.chat.id, "❌ Некорректный номер напоминания")

@bot.message_handler(commands=["edit"])
def edit_reminder(m):
    uid = str(m.chat.id)
    args = m.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.send_message(m.chat.id, "❌ Используй: /edit <номер>")
        return
    idx = int(args[1])-1
    reminders = data.get(uid, [])
    if 0 <= idx < len(reminders):
        bot.send_message(m.chat.id, f"✏️ Введи новый текст для напоминания {idx+1}:")
        bot.register_next_step_handler(m, lambda msg, i=idx: save_edit(msg, i))
    else:
        bot.send_message(m.chat.id, "❌ Некорректный номер напоминания")

def save_edit(m, idx):
    uid = str(m.chat.id)
    data[uid][idx]["text"] = m.text
    save_data(data)
    bot.send_message(m.chat.id, f"✅ Напоминание {idx+1} обновлено!")

# -----------------------
# Отправка напоминаний
# -----------------------
def send_reminder(uid, reminder):
    bot.send_message(uid, f"⏰ Напоминание:\n\n{reminder['text']}\n"
                          f"Используй команды:\n/done — я сделал\n/delay <минут> — отложить")
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
print("Бот запущен! Полный функционал: /list, /done, /delay, /delete, /edit")
bot.infinity_polling()