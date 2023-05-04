from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    departure_at = State()  # 'When? ')

    return_at = State()  # 'Back? ')

    origin = State()  # 'From? ')

    destination = State()  # 'To? ')
