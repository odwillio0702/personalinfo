import threading
import time
from keyboards import done_delay_keyboard

def start_scheduler(bot, data, send_func):
    def loop():
        while True:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            weekday = datetime.now().strftime("%A")

            for uid, reminders in data.items():
                for r in reminders:
                    if r["time"] == now and weekday in r["days"] and not r["done"]:
                        send_func(bot, int(uid), r)
            time.sleep(60)

    threading.Thread(target=loop, daemon=True).start()