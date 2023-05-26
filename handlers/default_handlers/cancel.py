from loader import bot


@bot.message_handler(state="*", commands=['cancel'])
def _any_state(message):
    """ Функция для реализации команда Cancel"""
    bot.send_message(message.chat.id, "*Ваш ввод был отменен .*", parse_mode="MarkDown")
    bot.delete_state(message.from_user.id, message.chat.id)