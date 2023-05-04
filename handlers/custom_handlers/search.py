import requests
from telebot import custom_filters
# from background import keep_alive  # импорт функции для поддержки работоспособности
from telegram_bot_calendar import DetailedTelegramCalendar

import config_data.config
from loader import bot
from states.get_states import MyStates


@bot.message_handler(commands=['start'])
def start(message):
    bot.set_state(message.from_user.id, MyStates.departure_at, message.chat.id)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id,
                     f"Когда вы хотите лететь? ",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Когда вы хотите лететь? ",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.add_data(result) as data:
            data['departure_at'] = result


#
# @bot.message_handler(state="*", commands=['cancel'])
# def any_state(message):
#     """
#     Cancel state
#     """
#     bot.send_message(message.chat.id, "Ваш ввод был отменен .")
#     bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.departure_at)
def origin_get(message):
    bot.send_message(message.chat.id, 'Откуда вы хотите летит, название город в формате: MOW? ')
    bot.set_state(message.from_user.id, MyStates.origin, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['departure_at'] = message.text


@bot.message_handler(state=MyStates.origin)
def get_destination(message):
    bot.send_message(message.chat.id, "Куда вы хотите летит, название город в формате: MOW?")
    bot.set_state(message.from_user.id, MyStates.destination, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = message.text


@bot.message_handler(state=MyStates.destination)
def return_at_age(message):
    bot.send_message(message.chat.id, "Когда вы хотите прилетит, дата в формате: 2023-01-30? ")
    bot.set_state(message.from_user.id, MyStates.return_at, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['destination'] = message.text


# result
@bot.message_handler(state=MyStates.return_at)
def ready_for_answer(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        currency = 'rub'
        limit = 10
        token = config_data.config.API_KEY
        params = {
            'origin': data['origin'],
            'destination': data['destination'],
            'currency': currency,
            'departure_at': data['departure_at'],
            'return_at': message.text,
            'limit': limit,
            'token': token
        }

        response = requests.get('http://api.travelpayouts.com/v1/prices/cheap?', params=params)
        # response_0 = requests.get('https://api.travelpayouts.com/aviasales_resources/v3/cities.json?locale=ru')
        # print(response_0.json())
        if 200 <= response.status_code <= 399:
            result = response.json()
            with open('received_data.json', 'w+') as file:
                file.write(str(result))
            trips = (result['data'])

            return bot.send_message(message.chat.id, str(trips))

        result = response.json()
        with open('received_data.json', 'w+') as file:
            file.write(str(result))
        trips = ([result['data']['destination']])

        bot.send_message(message.chat.id, str(trips), parse_mode="html")
        bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['help'])
def help_handler(message):
    if message.text == "/help":
        bot.send_message(message.chat.id, "Напиши help")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

if __name__ == '__main__':
    # keep_alive()

    bot.polling(none_stop=True, interval=0)
