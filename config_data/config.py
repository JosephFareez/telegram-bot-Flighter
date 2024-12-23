import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
try:
    load_dotenv(find_dotenv())
except FileNotFoundError:
    print("Warning: .env file not found. Some features may not work as expected.")

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# Define default commands
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Список команд и их описание"),
    ("search_low_price", "Поиск дешёвые билеты "),
    ("search_month", "поиск билеты в течение месяца"),
    ("search_non_stop_tickets", "поиск самых дешевых билетов без пересадок"),
    ("start_mini_app", "start_mini_app"),
    ("cancel", "Отмена поиска"),
    ("history", "История поиска")
)
