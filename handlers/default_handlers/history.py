from loader import bot
from database.history_db import db_create


@bot.message_handler(commands=['history'])
def _history_req(message):
    user_id = message.chat.id
    history = db_create(user_id, "New message", retrieve=True)
    bot.send_message(message.chat.id, history, parse_mode="MarkDown")
