from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


def fly_date():
    calendar, step = DetailedTelegramCalendar().build()
    return calendar, step


def fly_back_date():
    calendar, step = DetailedTelegramCalendar().build()
    return calendar, step
