from telebot.types import Message
from keyboards.inline import get_main_menu, get_first_setup_menu
from loader import bot
from database.common.models import Student


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    student, _ = Student.create_or_update(
        telegram_id=message.chat.id,
        telegram_full_name=message.from_user.full_name,
        telegram_username=message.from_user.username,
    )
    if student.text_type is not None and student.question_type is not None:
        bot.send_message(
            message.chat.id,
            f"С возвращением, {message.from_user.full_name}!",
            reply_markup=get_main_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Добро пожаловать в дневник чтения Библии курса Основ Веры!\n"
            "Пожалуйста, выберите режим чтения, в будущем вы сможете его изменить в меню настроек.",
            reply_markup=get_first_setup_menu()
        )
