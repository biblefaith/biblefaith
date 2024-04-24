from telebot.handler_backends import State, StatesGroup

# source_airport_code example: BOM
# destination_airport_code example: DEL
# date: example 2021-12-31
# num_adults
# num_seniors Number of Seniors (with age 65 and over)
# class_of_service ECONOMY | PREMIUM_ECONOMY | BUSINESS | FIRST

class UserAnswerState(StatesGroup):
    answer = State()
