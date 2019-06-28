import time
import datetime


def get_current_time_millis():
    return int(round(time.time() * 1000))


def get_hour_minute():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    t = str(hour)+":"+str(minute)
    return t


def get_date():
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    t = str(day)+"/"+str(month)+"/"+str(year)
    return t
