from loader import bot
# from database.common.models import HelpMessages
from config_data import config
from keyboards.inline import get_main_menu
from utils.functions import edit_message_reply_markup

def notify_user_message_forwarded(message):
    # Предполагаем, что у вас уже есть функция для генерации главного меню
    bot.send_message(message.chat.id, "Ваш вопрос отправлен администраторам. Ожидайте ответа.", reply_markup=get_main_menu())


def forward_message_to_admins(message):
    formatted_message = f"Сообщение от пользователя с ID {message.chat.id}:\n\n{message.text}"
    bot.send_message(config.ADMIN_CHAT_ID, formatted_message)
    notify_user_message_forwarded(message)


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def bot_help(call):
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Напишите ваш вопрос, и наш администратор поможет вам как можно скорее.")
    bot.register_next_step_handler(call.message, forward_message_to_admins)
