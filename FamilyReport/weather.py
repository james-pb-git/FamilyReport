from collections import Counter
from data import conf
from utils import *
import requests


def summarize_weather(list_weather):
    weather_cnt = Counter(list_weather)
    max_cnt = -1
    weather_summary = ''
    for v in weather_cnt:
        if weather_cnt[v] > max_cnt:
            max_cnt = weather_cnt[v]
            weather_summary = v
    return weather_summary


def get_weather(self):
    payload = {'id': conf.city_id,
               'appid': conf.weather_app_id,
               'units': 'metric',
    }
    weather_url = conf.weather_url
    weather_response = requests.get(weather_url, params=payload)
    weather_response.raise_for_status()  # If not 200, raise exception
    res = weather_response.json()
    weather_of_date = dict()
    for item in res['list']:
        str_time = utc_to_est(item['dt'])
        date_forecasted = str_time.split(" ")[0]
        temp = round(item['main']['temp'], 1)
        weather = item['weather'][0]['main'] + " (" + item['weather'][0]['description'] + ")"
        if date_forecasted not in weather_of_date:
            weather_of_date[date_forecasted] = {'min_temp': temp,
                                               'max_temp': temp,
                                               'weather': [weather]}
        else:
            weather_of_date[date_forecasted]['min_temp'] = min(temp,
                                                              weather_of_date[date_forecasted]['min_temp'])
            weather_of_date[date_forecasted]['max_temp'] = max(temp,
                                                              weather_of_date[date_forecasted]['max_temp'])
            weather_of_date[date_forecasted]['weather'].append(weather)
    for k, v in weather_of_date.items():
        v['weather'] = summarize_weather(v['weather'])
    sorted_weather = sorted(weather_of_date.items(), key=lambda x: x[0])
    return sorted_weather
