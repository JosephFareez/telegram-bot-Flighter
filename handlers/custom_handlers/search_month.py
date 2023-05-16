from datetime import datetime
import json
import requests
from telebot import custom_filters
# from background import keep_alive  # импорт функции для поддержки работоспособности
import config_data.config
from loader import bot
from states.get_states import MyStates


# def get_cities():
#
#     """Функция загрузки коды города в формате JSON"""
#     response_0 = requests.get('https://api.travelpayouts.com/aviasales_resources/v3/cities.json?locale=ru')
#     with open("cities.json", "w+", encoding="UTF-8") as cities:
#         cities.write(response_0.text)


def find_country_code(city_name, file_path="cities.json"):
    """Функция для поиска города вводимое пользователю в файле JSON """
    with open(file_path, "r", encoding="utf-8") as f:
        cities = json.load(f)
        for city in cities:
            if city['name'] == city_name:
                return city["code"]
        return "Город не найден"


@bot.message_handler(commands=['search_month'])
def search(message):
    """Функция start для получения город вылета"""
    bot.set_state(message.from_user.id, MyStates.origin, message.chat.id)
    bot.send_message(message.chat.id, f" *Привет, {message.from_user.first_name}, Введите город вылета: *",
                     parse_mode="MarkDown")

    find_country_code(message)


@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """Cancel state"""
    bot.send_message(message.chat.id, "*Ваш ввод был отменен .*", parse_mode="MarkDown")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.origin)
def get_destination(message):
    """Функция для получения город перелета"""
    bot.send_message(message.chat.id, "*Введите город прилета: *", parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.destination, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = find_country_code(message.text)


@bot.message_handler(state=MyStates.destination)
def get_departure_date(message):
    """Функция для получения дата вылета"""
    bot.send_message(message.chat.id, "*Введите дата вылета: *", parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.departure_at, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = find_country_code(message.text)


# result
@bot.message_handler(state=MyStates.departure_at)
def redy_to_answer(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['departure_at'] = message.text
        currency = 'rub'
        limit = 30
        token = config_data.config.API_KEY
        sorting = 'flights'
        origin = data['origin']
        destination = data['destination']
        departure_at = data['departure_at']

        params = {
            'origin': origin,
            'destination': destination,
            'departure_at': departure_at,
            'currency': currency,
            'limit': limit,
            'token': token,
            'sorting': sorting
        }

        response = requests.get('https://api.travelpayouts.com/v1/prices/calendar?', params=params)
        # print(response)

        if 200 <= response.status_code <= 399:
            result = response.json()
            with open('received_data.json', 'w+') as file:
                file.write(str(result))
                if file.__sizeof__() > 0:
                    trips = next(iter([result['data']]))
                    for flights in trips.values():
                        for flight in flights.values():
                            bot.send_message(message.chat.id, f"Цена: {flight['price']} рублей\n"
                                                              f"Авиакомпания: {flight['airline']}\n"
                                                              f"Откуда:{origin}({datetime.strptime(flight['departure_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')})\n"
                                                              f"Куда: {destination} ({datetime.strptime(flight['return_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')})\n"
                                                              f"Ссылка на билет: https://www.aviasales.ru/search/{origin}"
                                                              f"{departure_at}"
                                                              f"{destination}""1\n\n")

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
