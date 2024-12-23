from telebot import types
from loader import bot
from handlers.custom_handlers import search_low_price
from handlers.custom_handlers import search_month
from handlers.custom_handlers import search_non_stop_tickets
from handlers.default_handlers import help, cancel, history
from database.history_db import db_create


@bot.message_handler(commands=["start"])
def main_menu_markup(message):
    """Функция для создания кнопок с описанием каждой кнопкой"""
    db_create(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('По датам')
    item2 = types.KeyboardButton('Переделах месяца')
    item3 = types.KeyboardButton('Без пересадок')
    item4 = types.KeyboardButton('/help')
    item5 = types.KeyboardButton('/cancel')
    item6 = types.KeyboardButton('/history')
    item7 = types.KeyboardButton('О боте')
    item8 = types.KeyboardButton('start_mini_app')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} Выберите вид поиска билетов:",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    """Функция реагирует на нажатие кнопками возвышает соответствующий команда для кнопки"""
    if message.chat.type == 'private':
        if message.text == 'По датам':
            search_low_price._search_low_price(message)
            db_create(message.chat.id, message.text)

        elif message.text == 'Переделах месяца':
            search_month._search_month(message)

        elif message.text == 'Без пересадок':
            search_non_stop_tickets._search_non_stop_ticket(message)

        elif message.text == 'О боте':
            bot.send_message(message.chat.id, '*Бот для поиск авиа билетов на саите AviaSales "Это не официальный '
                                              'бот компании"*', parse_mode='MarkDown')
        elif message.text == '/help':
            help.bot_help()
            db_create(message.chat.id, message.text)

        elif message.text == '/cancel':
            cancel._any_state()
            db_create(message.chat.id, message.text)
        elif message.text == '/history':
            history._history_req()

        elif message.text == 'start_mini_app':
            mini_app_start.start_mini_app(message)
