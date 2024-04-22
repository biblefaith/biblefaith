from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message,
        "Это сообщение никто не видит, "
        "если вы хотите связаться с администратором, "
        "воспользуйтесь пожалуйста кнопкой помощи в меню /start\n\n"
        f"Сообщение: {message.text}",
    )
