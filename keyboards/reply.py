from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_help_menu_keyboard():
    # Создаем объект клавиатуры для главного меню
    keyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

    # Создаем кнопки для главного меню
    keyboard.add(KeyboardButton(text="Начать чтение"))
    keyboard.add(KeyboardButton(text="Настройки"))
    keyboard.add(KeyboardButton(text="Помощь"))

    return keyboard


