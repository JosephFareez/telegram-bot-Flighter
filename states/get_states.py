from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    depart_date = State()  # 'When? ')
    origin = State()  # 'From? ')
    destination = State()  # 'To? ')
    departure_at = State()  # 'Back? ')
    return_date = State()