import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('WEATHER_ACCESS_TOKEN')


def get_weather_description(response, day: str) -> str:
    if response.status_code == 200:
        data = response.json()
        if day == 'today':
            current_temperature = round(data['main']['temp'])
            weather_description = data['weather'][0]['description']
            max_current_temperature = round(data['main']['temp_max'])
            min_current_temperature = round(data['main']['temp_min'])
            wind = round(data['wind']['speed'])
            result = f"""Сейчас на улице {current_temperature}°C. {weather_description.capitalize()}.
Максимальная температура: {max_current_temperature}°C.
Минимальная температура: {min_current_temperature}°C.
Скорость ветра: {wind} м/с."""
            return result
        elif day == 'tomorrow':
            # температура с утра
            tomorrow_weather_morning = data['list'][2]
            temperature_tomorrow_morning = round(tomorrow_weather_morning['main']['temp'])
            description_tomorrow_morning = tomorrow_weather_morning['weather'][0]['description']
            # температура днём
            tomorrow_weather_daytime = data['list'][4]
            temperature_tomorrow_daytime = round(tomorrow_weather_daytime['main']['temp'])
            description_tomorrow_daytime = tomorrow_weather_daytime['weather'][0]['description']
            # температура вечером
            tomorrow_weather_evening = data['list'][7]
            temperature_tomorrow_evening = round(tomorrow_weather_evening['main']['temp'])
            description_tomorrow_evening = tomorrow_weather_evening['weather'][0]['description']
            # температура ночью
            tomorrow_weather_night = data['list'][10]
            temperature_tomorrow_night = round(tomorrow_weather_night['main']['temp'])
            description_tomorrow_night = tomorrow_weather_night['weather'][0]['description']
            result = f"""Погода на завтра.
Температура с утра: {temperature_tomorrow_morning}°C. {description_tomorrow_morning.capitalize()}.
Температура днём: {temperature_tomorrow_daytime}°C. {description_tomorrow_daytime.capitalize()}.
Температура вечером: {temperature_tomorrow_evening}°C. {description_tomorrow_evening.capitalize()}.
Температура ночью: {temperature_tomorrow_night}°C. {description_tomorrow_night.capitalize()}."""
            return result
        else:
            return 'Не удалось получить прогноз погоды.'


def get_weather_forecast(city: str, day='today') -> str:
    if day == 'today':
        current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&APPID={api_key}"
        response = requests.get(current_weather_url)
        return get_weather_description(response=response, day=day)
    elif day == 'tomorrow':
        tomorrow_weather_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&lang=ru&units=metric&APPID={api_key}'
        response = requests.get(tomorrow_weather_url)
        return get_weather_description(response=response, day=day)
    else:
        return "Не удалось получить прогноз погоды"

