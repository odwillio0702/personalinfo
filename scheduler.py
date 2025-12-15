
import time
import threading
from datetime import datetime
from keyboards import done_keyboard

def start_scheduler(bot, storage):
    def loop():
        while True:
            now = datetime.now().strftime("%H:%M")
            weekday = datetime.now().strftime("%A")

            for uid, reminders in storage.items():
                for r in reminders:
                    if r["time"] == now and weekday in r["days"] and not r["done"]:
                        send(bot, uid, r)
            time.sleep(60)

    threading.Thread(target=loop, daemon=True).start()

def send(bot, uid, reminder):
    bot.send_message(
        uid,
        f"⏰ Напоминание:\n\n{reminder['text']}",
        reply_markup=done_keyboard()
    )

    def repeat():
        time.sleep(600)
        if not reminder["done"]:
            send(bot, uid, reminder)

    threading.Thread(target=repeat).start()
