import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)
