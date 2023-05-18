import json


def find_country_code(city_name, file_path="cities.json"):
    """Функция для поиска города вводимое пользователю в файле JSON """
    with open(file_path, "r", encoding="utf-8") as f:
        cities = json.load(f)
        for city in cities:
            if city['name'] == city_name:
                return city["code"]
        return "Город не найден"


# def get_cities():
#
#     """Функция загрузки коды города в формате JSON"""
#     response_0 = requests.get('https://api.travelpayouts.com/aviasales_resources/v3/cities.json?locale=ru')
#     with open("cities.json", "w+", encoding="UTF-8") as cities:
#         cities.write(response_0.text)