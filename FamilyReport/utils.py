from datetime import datetime
from datetime import date
from dateutil import tz


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def utc_to_est(utc_timestamp):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('EST')
    utc_time = datetime.fromtimestamp(utc_timestamp)
    utc_time = utc_time.replace(tzinfo=from_zone)
    local_time = utc_time.astimezone(to_zone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')


def num2ord(n):
    return str(n)+("th" if 4 <= n%100 <= 20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))