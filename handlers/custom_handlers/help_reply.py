from loader import bot
from config_data import config
import re

def extract_user_id(text):
    match = re.search(r'ID (\d+):', text)
    return int(match.group(1)) if match else None


@bot.message_handler(content_types=['text'], func=lambda message: message.chat.id == int(config.ADMIN_CHAT_ID) and message.reply_to_message)
def handle_admin_reply(message):
    # Предполагается, что оригинальное сообщение пользователя содержало его ID в тексте
    original_content = message.reply_to_message.text
    user_id = extract_user_id(original_content)  # Функция для извлечения user_id из текста
    if user_id:
        bot.send_message(user_id, f"Сообщение от администратора\n\n{message.text}")
    else:
        bot.send_message(message.chat.id, "Не удалось определить пользователя для ответа.")
