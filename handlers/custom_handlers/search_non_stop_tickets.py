import json
from time import strftime
import requests
from telebot import custom_filters
import config_data.config
from loader import bot
from states.get_states import MyStates
from datetime import datetime
from database.city_finder import find_country_code


@bot.message_handler(commands=['search_non_stop_tickets'])
def _search_non_stop_ticket(message):
    """Функция start для получения Город вылета """
    bot.set_state(message.from_user.id, MyStates.origin, message.chat.id)
    bot.send_message(message.chat.id, f" *Введите город вылета: *",
                     parse_mode="MarkDown")
    find_country_code(message)


@bot.message_handler(state="*", commands=['cancel'])
def _any_state(message):
    """Cancel state"""
    bot.send_message(message.chat.id, "*Ваш ввод был отменен .*", parse_mode="MarkDown")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.origin)
def _get_destination(message):
    """Функция для получения город прилета """
    bot.send_message(message.chat.id, '*Введите город прилета: *',
                     parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.destination, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = find_country_code(message.text)


@bot.message_handler(state=MyStates.destination)
def _get_departure_date(message):
    """Функция для получения дата вылета"""
    bot.send_message(message.chat.id, strftime("*Введите дата вылета: *"), parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.depart_date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['destination'] = find_country_code(message.text)


@bot.message_handler(state=MyStates.depart_date)
def _ready_to_answer(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['depart_date'] = message.text
        currency = 'rub'
        limit = 30
        token = config_data.config.API_KEY
        sorting = 'price'
        origin = data['origin']
        destination = data['destination']
        depart_date = data['depart_date']

        params = {
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'currency': currency,
            'limit': limit,
            'token': token,
            'sorting': sorting,

        }

        response = requests.get('https://api.travelpayouts.com/v1/prices/direct?', params=params)

        if 200 <= response.status_code <= 399:
            result = response.json()

            with open('received_data.json', 'w+') as file:
                file.write(str(result))
                if file.__sizeof__() > 0:
                    trips = next(iter([result['data']]))
                    for flights in trips.values():
                        for flight in flights.values():
                            departure = ''.join(filter(str.isalnum, depart_date))
                            bot.send_message(message.chat.id, f"Цена: {flight['price']} рублей\n"
                                                              f"Авиакомпания: {flight['airline']}\n"
                                                              f"Туда: {origin} --> {destination} ({datetime.strptime(flight['departure_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')})\n"
                                                              f"Обратно: {destination} --> {origin} ({datetime.strptime(flight['return_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')})\n"
                                                              f"Ссылка на билет: https://www.aviasales.ru/search/{origin}"
                                                              f"{departure}"
                                                              f"{destination}""1?\n\n")

                else:
                    bot.send_message(message.chat.id, "*Нет доступных билетов на выбранные даты.*",
                                     parse_mode="MarkDown")
        else:
            print(response)
            bot.send_message(message.chat.id, "*Ошибка при запросе к API. Попробуйте позже.*",
                             parse_mode="MarkDown")
    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
