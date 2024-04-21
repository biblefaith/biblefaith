from config_data.config import DEFAULT_COMMANDS
from loader import bot
from keyboards.reply import get_help_menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def bot_help(call):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(call.message.chat.id, "\n".join(text))
