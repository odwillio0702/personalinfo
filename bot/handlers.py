from bot.database import add_user, update_views

def register_user(user_data: dict):
    """
    Сохраняем или обновляем пользователя в базе данных
    """
    user_id = user_data.get("id")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    username = user_data.get("username", "")
    add_user(user_id, first_name, last_name, username)

def send_profile(user_id: int):
    """
    Возвращает данные профиля для веб-приложения
    """
    return update_views(user_id)