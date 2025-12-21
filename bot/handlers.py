from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database import add_user, increment_likes, increment_views, get_user_stats
from bot.main import bot

def register_user(user):
    add_user(user.id, user.username)
    increment_views(user.id)  # считаем, что открытие профиля = просмотр

def send_profile(chat_id, user_id):
    stats = get_user_stats(user_id)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(f"❤️ {stats['likes']}", callback_data=f"like_{user_id}")
    )
    bot.send_message(chat_id, f"Профиль @{user_id}\nПросмотры: {stats['views']}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("like_"))
def handle_like(call):
    user_id = int(call.data.split("_")[1])
    likes = increment_likes(user_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=InlineKeyboardMarkup().add(
                                      InlineKeyboardButton(f"❤️ {likes}", callback_data=f"like_{user_id}")
                                  ))
    bot.answer_callback_query(call.id, text="Вы поставили лайк!")