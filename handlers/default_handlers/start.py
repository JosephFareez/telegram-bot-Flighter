from telebot.types import Message


from keyboards.inline import main_menu
from loader import bot


@bot.message_handler(commands=["start"])
def start(message):
    pass

