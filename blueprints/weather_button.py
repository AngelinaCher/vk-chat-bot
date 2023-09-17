from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from database.db_connection import db_collection
from utils.weather import get_weather_forecast

bp = Blueprint()
bp.on.vbml_ignore_case = True


# Обработка погоды
@bp.on.private_message(text="Погода")
@bp.on.private_message(payload={"cmd": "weather"})
async def weather_handler(message: Message):
    keyboard = (
        Keyboard()
        .add(Text(label="Сегодня", payload={"cmd": "weather_today"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(label="Завтра", payload={"cmd": "weather_tomorrow"}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text(label="Назад", payload={"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer("Погода на сегодня или завтра?", keyboard=keyboard)


# Погода на сегодня
@bp.on.private_message(text="Сегодня")
@bp.on.private_message(payload={"cmd": "weather_today"})
async def today_weather_handler(message: Message):
    user_id = message.from_id
    user_in_db = db_collection.find_one({'_id': user_id})
    if user_in_db:
        city = user_in_db.get('city')
        await message.answer(get_weather_forecast(city=city, day='today'))
    else:
        await message.answer("Произошла ошибка. Попробуйте сменить город.")


# Погода на завтра
@bp.on.private_message(text="Завтра")
@bp.on.private_message(payload={"cmd": "weather_tomorrow"})
async def tomorrow_weather_handler(message: Message):
    user_id = message.from_id
    user_in_db = db_collection.find_one({'_id': user_id})
    if user_in_db:
        city = user_in_db.get('city')
        await message.answer(get_weather_forecast(city=city, day='tomorrow'))
    else:
        await message.answer("Произошла ошибка. Попробуйте сменить город.")
