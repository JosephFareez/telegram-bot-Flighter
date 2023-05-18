from loader import bot
import handlers  # noqa
# from background import keep_alive # импорт функции для поддержки работоспособности


if __name__ == "__main__":
    # keep_alive()
    bot.infinity_polling()
