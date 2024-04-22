from loguru import logger
from keyboards.inline import get_question_type, get_text_type, get_main_menu
from loader import bot
from database.common.models import Student
from utils.functions import edit_message_reply_markup

# Настройка логирования
logger.add("bot.log", format="{time} {level} {message}", level="INFO")


# Определение констант
BIBLE_TYPES = ['rst', 'nrt']
QUESTION_TYPES = ['beginner', 'advanced']


@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def get_settings(call):
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text="Выберите перевод Библии", reply_markup=get_text_type())
    logger.info("Отправлено сообщение с выбором перевода Библии")


@bot.callback_query_handler(func=lambda call: call.data in BIBLE_TYPES)
def set_bible_type(call):
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    Student.create_or_update(telegram_id=call.message.chat.id, text_type=call.data)
    bot.send_message(call.message.chat.id, "Выберите тип вопросов", reply_markup=get_question_type())


@bot.callback_query_handler(func=lambda call: call.data in QUESTION_TYPES)
def set_question_type(call):
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    Student.create_or_update(telegram_id=call.message.chat.id, question_type=call.data)
    bot.send_message(call.message.chat.id, "Настройки сохранены", reply_markup=get_main_menu())
