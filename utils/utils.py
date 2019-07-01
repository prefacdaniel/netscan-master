import time
import datetime


def get_current_time_millis():
    try:
        return int(round(time.time() * 1000))
    except:
        print("Exception - utils - get_current_time_millis")


def get_hour_minute():
    try:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        t = str(hour)+":"+str(minute)
        return t
    except:
        print("Exception - utils - get_hour_minute")


def get_date():
    try:
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year
        t = str(day)+"/"+str(month)+"/"+str(year)
        return t
    except:
        print("Exception - utils - get_date")
