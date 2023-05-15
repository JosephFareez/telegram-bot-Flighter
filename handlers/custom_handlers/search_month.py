import json
<<<<<<< HEAD
import requests
from telebot import custom_filters
=======
import datetime
import requests
from telebot import custom_filters

>>>>>>> origin/master
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


<<<<<<< HEAD
<<<<<<<< HEAD:handlers/custom_handlers/search_month.py
@bot.message_handler(commands=['search_month'])
========
@bot.message_handler(commands=['search_low_price'])
>>>>>>>> origin/master:handlers/custom_handlers/search_low_price.py
def search(message):
    """Функция start для получения город вылета """
=======
@bot.message_handler(commands=['search_month'])
def search(message):
    """Функция start для получения дата вылета """
>>>>>>> origin/master
    bot.set_state(message.from_user.id, MyStates.origin, message.chat.id)
    bot.send_message(message.chat.id, f" *Привет, {message.from_user.first_name}, Введите город вылета: *",
                     parse_mode="MarkDown")

    find_country_code(message)


<<<<<<< HEAD
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """Cancel state"""
    bot.send_message(message.chat.id, "*Ваш ввод был отменен .*", parse_mode="MarkDown")
    bot.delete_state(message.from_user.id, message.chat.id)
=======
# @bot.message_handler(state="*", commands=['cancel'])
# def any_state(message):
#     """Cancel state"""
#     bot.send_message(message.chat.id, "*Ваш ввод был отменен .*", parse_mode="MarkDown")
#     bot.delete_state(message.from_user.id, message.chat.id)
>>>>>>> origin/master



@bot.message_handler(state=MyStates.origin)
def get_destination(message):
    """Функция для получения город перелета    """
    bot.send_message(message.chat.id, "*Введите город перелета: *", parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.destination, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = find_country_code(message.text)


<<<<<<< HEAD
@bot.message_handler(state=MyStates.destination)
def get_destination(message):
    """Функция для получения дата вылета"""
    bot.send_message(message.chat.id, "*Введите дата вылета: *", parse_mode="MarkDown")
    bot.set_state(message.from_user.id, MyStates.departure_date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['origin'] = find_country_code(message.text)

# result
@bot.message_handler(state=MyStates.departure_date)
=======

# result
@bot.message_handler(state=MyStates.destination)
>>>>>>> origin/master
def ready_for_answer(message):
    """Функция обработка ответ пользователя и получения ответа от API и направит его получению """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['destination'] = find_country_code(message.text)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data.get('destination') is None:
<<<<<<< HEAD
            bot.send_message(message.chat.id, "*Вы не указали пункт назначения. Введите /search_month для начала "
                                              "поиска.*", parse_mode="MarkDown")
            return
        else:
            currency = 'rub'
            limit = 30
            token = config_data.config.API_KEY
            sorting = 'departure_at'
            calendar_type = data.get('departure_date')

            params = {
                'origin': data['origin'],
                'destination': data['destination'],
                'calendar_type': calendar_type,
                'currency': currency,
                # 'return_at': message.text,
                'limit': limit,
                'token': token,
                'sorting': sorting,

            }

            response = requests.get('https://api.travelpayouts.com/v1/prices/calendar?', params=params)
            # print(response)

            if 200 <= response.status_code <= 399:
                result = response.json()
                with open('received_data.json', 'w+') as file:
                    file.write(str(result))
                trips = next(iter([result['data']]))
                for flight in trips.values():
                    for i_key in flight.values():
<<<<<<<< HEAD:handlers/custom_handlers/search_month.py
                        bot.send_message(message.chat.id, json.dumps(i_key, indent='\n'), parse_mode="html")

========
                        bot.send_message(message.chat.id, json.dumps(i_key, indent=4), parse_mode="html")
                        # print([i_key['price'],
                        #        i_key['airline'],
                        #        i_key['flight_number'],
                        #        i_key['departure_at'],
                        #        i_key['return_at']])

                        # bot.send_message(message.chat.id, str((i_key['price'],
                        #                                        i_key['airline'],
                        #                                        i_key['flight_number'],
                        #                                        i_key['departure_at'],
                        #                                        i_key['return_at']
                        #                                        )))

            # result = response.json()
            # with open('received_data.json', 'w+') as file:
            #     file.write(str(result))
            # trips = next(iter([result['data']]))

            # bot.send_message(message.chat.id, json.dumps(trips, indent=8), parse_mode="html")
>>>>>>>> origin/master:handlers/custom_handlers/search_low_price.py
            bot.delete_state(message.from_user.id, message.chat.id)

        bot.add_custom_filter(custom_filters.StateFilter(bot))
        bot.add_custom_filter(custom_filters.IsDigitFilter())

=======
            bot.send_message(message.chat.id, "Вы не указали пункт назначения. Введите /start для начала поиска.")
            return
        else:
            currency = 'rub'
            limit = 10
            token = config_data.config.API_KEY
            departure_at = datetime.datetime.today().isoformat()
            params = {
                'origin': data['origin'],
                'destination': data['destination'],
                'departure_at': departure_at,
                'currency': currency,
                'limit': limit,
                'token': token
            }

            response = requests.get('https://api.travelpayouts.com/v1/prices/calendar?', params=params)
            print(response)

            if 200 <= response.status_code <= 399:
                result = response.json()
                with open('received_data.json', 'w') as file:
                    file.write(str(result))
                trips = (result['data'])

                return bot.send_message(message.chat.id, str(trips))

            result = response.json()
            with open('received_data.json', 'w') as file:
                file.write(str(result))
            trips = str([result['data']])

            bot.send_message(message.chat.id, json.dumps(trips, indent=8), parse_mode="html")
            bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['help'])
def help_handler(message):
    if message.text == "/help":
        bot.send_message(message.chat.id, "Напиши help")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
>>>>>>> origin/master
