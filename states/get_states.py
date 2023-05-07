

from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    departure_at = State()  # 'When? ')
    origin = State()  # 'From? ')
    destination = State()  # 'To? ')
    departure_date = State()  # 'Back? ')