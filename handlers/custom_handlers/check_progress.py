from keyboards.inline import get_main_menu
from utils.functions import edit_message_reply_markup
from loader import bot
from database.common.models import Student

# Определяем обработчик для вызова главного меню
@bot.callback_query_handler(func=lambda call: call.data == 'view_progress')
def main_menu_callback(call):
    # Отправляем сообщение с главным меню
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    progress = Student.get(telegram_id=call.message.chat.id).get_current_progress()
    day_number = progress['day_number']
    if not day_number:
        bot.send_message(call.message.chat.id, "Вы еще не начали чтение.",
                         reply_markup=get_main_menu())
        return
    bot.send_message(call.message.chat.id, f"Ваш текущий день чтения:\n{day_number} из 49", reply_markup=get_main_menu())
