import os
from dotenv import load_dotenv
from vkbottle.api import API

load_dotenv()

TOKEN = os.getenv("TOKEN")

USERNAME_DB = os.getenv('USERNAME_DB')
PASSWORD = os.getenv('PASSWORD')

api = API(os.getenv("USER_ACCESS_TOKEN"))

api_key_weather = os.getenv('WEATHER_ACCESS_TOKEN')
