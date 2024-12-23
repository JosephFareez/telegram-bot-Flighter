from loader import bot
import handlers  # noqa
from background import keep_alive

# from background import keep_alive  # Uncomment this line if needed

if __name__ == "__main__":
    # Uncomment the line below if needed
    keep_alive()

    # Import the test module conditionally
    if __name__ == "main":
        bot.infinity_polling()
