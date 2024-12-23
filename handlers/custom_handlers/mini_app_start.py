from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import os
import config_data.config
from loader import bot
@bot.message_handler(commands=['start_mini_app'])
def start_handler(message):
    # Create a keyboard with a Web App button
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = KeyboardButton(
        text="Open TON MiniApp",
        web_app=WebAppInfo(url="https://513bedf4-dc58-49e4-bc05-fd2d744b2fbf-00-27ngp6ss6epzo.riker.replit.dev/")  # Replace with your MiniApp URL
    )
    keyboard.add(web_app_button)

    bot.send_message(
        message.chat.id,
        "Welcome to TON MiniApp! Click the button below to get started.",
        reply_markup=keyboard
    )
