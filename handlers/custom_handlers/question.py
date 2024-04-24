from utils.functions import edit_message_reply_markup
from loader import bot
from database.common.models import Student
from database.common.models import Diary
from states.answerstate import UserAnswerState
from keyboards.inline import get_main_menu

# Определяем обработчик для вызова главного меню
@bot.callback_query_handler(func=lambda call: call.data == 'get_question')
def main_menu_callback(call):
    # Отправляем сообщение с главным меню
    edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    set = Student.select().where(Student.telegram_id == call.message.chat.id).get()
    question_entity = (Diary
                  .select()
                  .where(
                      (Diary.day_number == set.day_number) & 
                      (Diary.content_ordering_value == set.ordering_number) & 
                      (Diary.content_category == "question") &
                      (Diary.content_variety == set.question_type)
                  )
                  .order_by(Diary.created_at.desc())  # Order by created_at descending
                  .get_or_none())  # Get the first record of the resulting query
    if question_entity:
        question = question_entity.content_value
        bot.set_state(call.message.chat.id, UserAnswerState.answer)
        bot.send_message(call.message.chat.id, question)
    else:
        bot.send_message(call.message.chat.id, "Вопросы по выбранному тексту в разработке.", reply_markup=get_main_menu())
