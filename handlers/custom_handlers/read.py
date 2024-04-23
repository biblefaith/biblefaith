from keyboards.inline import get_question_menu
from utils.functions import edit_message_reply_markup
from loader import bot
from database.common.models import Student

# Определяем обработчик для вызова главного меню
@bot.callback_query_handler(func=lambda call: call.data == 'start_reading')
def main_menu_callback(call):
    # Отправляем сообщение с главным меню
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    text = Student.get(telegram_id=call.message.chat.id).get_current_text()
    bot.send_message(call.message.chat.id, text, reply_markup=get_question_menu())
