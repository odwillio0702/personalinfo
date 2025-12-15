from telebot import types

def done_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Я сделал", callback_data="done"))
    return kb
