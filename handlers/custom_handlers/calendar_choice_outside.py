from loguru import logger
from telebot.types import Message

import states
from loader import bot


@bot.message_handler(func=lambda message: 'calendar_choice')
@logger.catch
def outside_algorithm(message: Message) -> None:
    """Функция перехватывает сообщения при выборе с клавиатуры
    """
    bot.send_message(message.chat.id, 'Воспользуйтесь предложенным выбором.')
