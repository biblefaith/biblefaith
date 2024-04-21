from telebot.types import Message
from keyboards.inline import get_main_menu
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.full_name}!",
        reply_markup=get_main_menu()
    )
