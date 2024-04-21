from keyboards.inline import get_main_menu
from loader import bot


# Определяем обработчик для вызова главного меню
@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def main_menu_callback(call):
    # Отправляем сообщение с главным меню
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=get_main_menu())
