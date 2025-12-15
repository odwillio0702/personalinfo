from telebot import types

# Кнопка "Я сделал"
def done_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("✅ Я сделал", callback_data="done"))
    return kb

# Кнопки "Я сделал" + "Отложить 10 минут"
def done_delay_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Я сделал", callback_data="done"),
        types.InlineKeyboardButton("⏰ Отложить на 10 минут", callback_data="delay10")
    )
    return kb
