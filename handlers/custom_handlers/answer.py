from keyboards.inline import get_next_question_menu
from keyboards.inline import get_main_menu
from loader import bot
from database.common.models import Student
from database.common.models import Diary
from database.common.models import Answer
from states.answerstate import UserAnswerState


# @bot.callback_query_handler(func=lambda call: call.data == 'save_answer')
@bot.message_handler(state=UserAnswerState.answer)
def process_answer(message):
    # Сохраняем ответ в модель Answer
    bot.set_state(message.chat.id, None)
    set = Student.select().where(Student.telegram_id == message.chat.id).get()
    answer = Answer.create(telegram_id=set.telegram_id, day_number = set.day_number, question_number = set.ordering_number, answer = message.text)
    answer.save()
    next_day_question_entity = (Diary
                .select()
                .where(
                    (Diary.day_number == set.day_number) & 
                    (Diary.content_ordering_value == set.ordering_number + 1) & 
                    (Diary.content_category == "question") &
                    (Diary.content_variety == set.question_type)
                )
                .order_by(Diary.created_at.desc())  # Order by created_at descending
                .get_or_none())  # Get the first record of the resulting query
    if next_day_question_entity:
        Student.create_or_update(telegram_id=message.chat.id, ordering_number=set.ordering_number + 1)
        # Переходим к следующему вопросу или завершаем
        bot.send_message(message.chat.id, "Ответ принят.", reply_markup=get_next_question_menu())
        return
    
    Student.create_or_update(telegram_id=message.chat.id, day_number=set.day_number + 1)
    bot.send_message(message.chat.id, "Вы завершили чтение на сегодня.", reply_markup=get_main_menu())
