from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    # Создаем объект клавиатуры для главного меню
    keyboard = InlineKeyboardMarkup()

    # Создаем кнопки для главного меню
    keyboard.add(InlineKeyboardButton(text="Начать чтение", callback_data="start_reading"))
    keyboard.add(InlineKeyboardButton(text="Настройки", callback_data="settings"))
    keyboard.add(InlineKeyboardButton(text="Помощь", callback_data="help"))
    keyboard.add(InlineKeyboardButton(text="Посмотреть прогресс", callback_data="view_progress"))

    return keyboard


def get_first_setup_menu():
    # Создаем объект клавиатуры для главного меню
    keyboard = InlineKeyboardMarkup()

    # Создаем кнопки для главного меню
    keyboard.add(InlineKeyboardButton(text="Настройки", callback_data="settings"))
    keyboard.add(InlineKeyboardButton(text="Помощь", callback_data="help"))

    return keyboard


def get_question_type():
    # Создаем объект клавиатуры для выбора типа текста
    keyboard = InlineKeyboardMarkup()

    # Создаем кнопки для выбора типа текста
    keyboard.add(InlineKeyboardButton("Для начинающих", callback_data="beginner"))
    keyboard.add(InlineKeyboardButton("Для опытных", callback_data="advanced"))

    return keyboard


def get_text_type():
    # Создаем объект клавиатуры для выбора типа текста
    keyboard = InlineKeyboardMarkup()

    # Создаем кнопки для выбора типа текста
    keyboard.add(InlineKeyboardButton("Синодальный перевод", callback_data="rst"))
    keyboard.add(InlineKeyboardButton("Современный перевод", callback_data="nrt"))
    return keyboard
