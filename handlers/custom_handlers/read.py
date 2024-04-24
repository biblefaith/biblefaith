from keyboards.inline import get_question_menu
from utils.functions import edit_message_reply_markup
from loader import bot
from database.common.models import Student
from database.common.models import Diary

# Определяем обработчик для вызова главного меню
@bot.callback_query_handler(func=lambda call: call.data == 'start_reading')
def main_menu_callback(call):
    # Отправляем сообщение с главным меню
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    set = Student.select().where(Student.telegram_id == call.message.chat.id).get()
    text_entry = (Diary
                  .select()
                  .where(
                      (Diary.day_number == set.day_number) & 
                      (Diary.content_category == "bible") &
                      (Diary.content_variety == set.text_type)
                  )
                  .order_by(Diary.created_at.desc())  # Order by created_at descending
                  .get())  # Get the first record of the resulting query
    text = text_entry.content_value
    bot.send_message(call.message.chat.id, text, reply_markup=get_question_menu())
