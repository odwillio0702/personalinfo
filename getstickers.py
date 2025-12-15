import telebot
import json

BOT_TOKEN = "7534968024:AAGzt6dSrfXJvDKBahWku5ZYsYd9HNhM-XA"  # вставь сюда токен
bot = telebot.TeleBot(BOT_TOKEN)

stickers_list = []

print("👆 Отправь стикеры из пакета этому боту. Для завершения введи /done")

@bot.message_handler(content_types=['sticker'])
def get_sticker(m):
    file_id = m.sticker.file_id
    if file_id not in stickers_list:
        stickers_list.append(file_id)
        print(f"✅ Добавлен: {file_id}")

@bot.message_handler(commands=['done'])
def finish(m):
    with open("stickers.json", "w") as f:
        json.dump(stickers_list, f, indent=4)
    print("🎉 Все стикеры сохранены в stickers.json")
    print(stickers_list)
    bot.stop_polling()

bot.infinity_polling()