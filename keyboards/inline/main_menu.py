
from telebot import types
from loader import bot

from handlers.custom_handlers import search_low_price
from handlers.custom_handlers import search_month
from handlers.custom_handlers import search_non_stop_tickets


@bot.message_handler(commands=["start"])
def main_menu_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('По датам')
    item2 = types.KeyboardButton('Переделах месяца')
    item3 = types.KeyboardButton('Без пересадок')
    item4 = types.KeyboardButton('О боте')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} Выберите вид поиска билетов:",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'По датам':
            search_low_price._search_low_price(message)

        elif message.text == 'Переделах месяца':
            search_month._search_month(message)

        elif message.text == 'Без пересадок':
            search_non_stop_tickets._search_non_stop_ticket(message)

        elif message.text == 'О боте':
            bot.send_message(message.chat.id, '*Бот для поиск авиа билетов на саите AviaSales "Это не официальный '
                                              'бот компании"*', parse_mode='MarkDown')
