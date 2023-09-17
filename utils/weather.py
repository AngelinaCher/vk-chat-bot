import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('WEATHER_ACCESS_TOKEN')


# Описание погоды на сегодня
def get_today_weather_description(city, data):
    result = ''
    current_weather = data['main']
    weather = data['weather'][0]
    wind_speed = data['wind']['speed']

    result += f'{city}\n'
    result += f"Сейчас на улице {round(current_weather['temp'])}°C. {weather['description'].capitalize()}\n"
    result += f"Максимальная температура: {round(current_weather['temp_max'])}°C\n"
    result += f"Минимальная температура: {round(current_weather['temp_min'])}°C"
    result += f"Скорость ветра: {round(wind_speed)} м/с"
    return result


# Описание погоды на завтра
def get_tomorrow_weather_description(city, data):
    times = [2, 4, 7, 10]
    descriptions = ['утром', 'днём', 'вечером', 'ночью']
    tomorrow_data = data['list']
    result = f"""{city}\n Погода на завтра"""
    for i in range(4):
        weather_data = tomorrow_data[times[i]]
        temperature = round(weather_data['main']['temp'])
        description = weather_data['weather'][0]['description'].capitalize()
        result += f"\nТемпература {descriptions[i]}: {temperature}°C. {description}"
    return result


# Получить описание прогноза погоды
def generate_weather_description(response, day: str, city: str) -> str:
    if response.status_code == 200:
        data = response.json()
        if day == 'today':
            return get_today_weather_description(city=city, data=data)
        elif day == 'tomorrow':
            return get_tomorrow_weather_description(city=city, data=data)
    else:
        return 'Не удалось получить прогноз погоды.'


# Получить прогноз погоды
def get_weather_forecast(city: str, day='today') -> str:
    if day == 'today':
        current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&APPID={api_key}"
        response = requests.get(current_weather_url)
        return generate_weather_description(response=response, day=day, city=city)
    elif day == 'tomorrow':
        tomorrow_weather_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&lang=ru&units=metric&APPID={api_key}'
        response = requests.get(tomorrow_weather_url)
        return generate_weather_description(response=response, day=day, city=city)
    else:
        return "Не удалось получить прогноз погоды"
