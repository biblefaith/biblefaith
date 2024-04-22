from loader import bot
from telebot.apihelper import ApiTelegramException
from loguru import logger


def edit_message_reply_markup(chat_id, message_id, reply_markup=None):
    try:
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=reply_markup)
    except ApiTelegramException as e:
        bot.send_message(chat_id, f"Ошибка при редактировании сообщения: {e}")
        logger.exception("Ошибка при редактировании сообщения")
