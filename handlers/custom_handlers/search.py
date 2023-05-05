import json

import requests
from telebot import custom_filters

# from background import keep_alive  # импорт функции для поддержки работоспособности
import config_data.config
from loader import bot
from states.get_states import MyStates


# def get_cities():

# """Функция загрузки коды города в формате JSON"""
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


@bot.message_handler(commands=['start'])
def search(message):
    """Функция start для получения дата вылета """
    bot.set_state(message.from_user.id, MyStates.departure_at, message.chat.id)
    bot.send_message(message.chat.id, f" *Привет, {message.from_user.first_name}, Когда вы хотите лететь? *",
                     parse_mode="MarkDown")
    find_country_code(message)


@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """Cancel state"""
    bot.send_message(message.chat.id, "*Ваш ввод был отменен .*", parse_mode="MarkDown")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.departure_at)
def origin_get(message):
    """Функция для получения город отправление """
    bot.send_message(message.chat.id, '*Откуда вы хотите лететь? *',
                     parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.origin, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['departure_at'] = message.text


@bot.message_handler(state=MyStates.origin)
def get_destination(message):
    """Функция для получения город перелета    """
    bot.send_message(message.chat.id, "*Куда вы хотите лететь, название город в формате: MOW?*", parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.destination, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = find_country_code(message.text)


@bot.message_handler(state=MyStates.destination)
def return_at_age(message):
    """Функция для получения дата возврата """
    bot.send_message(message.chat.id, "*Когда вы хотите прилететь? *", parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.return_at, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['destination'] = find_country_code(message.text)


# result
@bot.message_handler(state=MyStates.return_at)
def ready_for_answer(message):
    """Функция обработка ответ пользователя и получения ответа от API и направит его получению """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data.get('destination') is None:
            bot.send_message(message.chat.id, "Вы не указали пункт назначения. Введите /start для начала поиска.")
            return
        else:
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

            if 200 <= response.status_code <= 399:
                result = response.json()
                with open('received_data.json', 'w+') as file:
                    file.write(str(result))
                trips = (result['data'])

                return bot.send_message(message.chat.id, str(trips))

            result = response.json()
            with open('received_data.json', 'w+') as file:
                file.write(str(result))
            trips = str([result['data']['destination']])

            bot.send_message(message.chat.id, json.dumps(trips, indent=8), parse_mode="html")
            bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['help'])
def help_handler(message):
    if message.text == "/help":
        bot.send_message(message.chat.id, "Напиши help")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
