import os
from dotenv import load_dotenv
from vkbottle import BaseStateGroup, CtxStorage, Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle.bot import Bot, Message
from loguru import logger

from database.db_connection import db_collection
from weather import get_weather_forecast
from currency import exchange_rates

# отключение логгера
logger.disable('vkbottle')

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
ctx_storage = CtxStorage()


# Регистрация города
class CityState(BaseStateGroup):
    """ Сохранение стейтов для регистрации города """
    CITY_CONFIRMATION = 'CITY_CONFIRMATION'
    CITY_INDICATION = 'CITY_INDICATION'


# получить город из профиля
async def get_city_handler(message: Message):
    user_info = await bot.api.users.get(user_ids=message.from_id, fields=['city'])
    if user_info[0].city:
        city = user_info[0].city.title
        ctx_storage.set("city", city)
        await message.answer(f"Ваш город {city}?")
        await bot.state_dispenser.set(message.peer_id, CityState.CITY_CONFIRMATION)
    else:
        await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
        await bot.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)


# обработка кнопки "Начать"
@bot.on.private_message(text="Начать")
@bot.on.private_message(payload={"cmd": "start"})
async def start_handler(message: Message):
    existing_user = db_collection.find_one({"_id": message.from_id})
    if existing_user:
        keyboard = (
            Keyboard()
            .add(Text(label="Меню", payload={"cmd": "menu"}))
            .row()
            .add(Text(label="Сменить город", payload={"cmd": "change_city"}), color=KeyboardButtonColor.POSITIVE)
        ).get_json()
        await message.answer('Вы зарегистрированы. Введите "Меню" или нажмите на кнопку.', keyboard=keyboard)
    else:
        await get_city_handler(message=message)


# подтверждение города
@bot.on.private_message(state=CityState.CITY_CONFIRMATION)
async def city_confirmation_handler(message: Message):
    ctx_storage.set("confirmation", message.text)
    confirmation = ctx_storage.get("confirmation").lower()
    if confirmation == "да":
        city_name = ctx_storage.get("city")
        db_collection.delete_one({"_id": message.from_id})
        db_collection.insert_one({"_id": message.from_id, "city": city_name})
        keyboard = Keyboard().add(Text(label="Начать", payload={"cmd": "start"})).get_json()
        await message.answer("Ваш город успешно зарегистрирован!", keyboard=keyboard)
    elif confirmation == "нет":
        await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
        await bot.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)
    else:
        await message.answer('Пожалуйста, напишите "Да" или "Нет"')


# проверка города, указанного пользователем
@bot.on.private_message(state=CityState.CITY_INDICATION)
async def city_indication_handler(message: Message):
    existing_user = db_collection.find_one({"_id": message.from_id})
    if existing_user:
        db_collection.delete_one({"_id": message.from_id})
    ctx_storage.set("indication", message.text.capitalize())
    city = ctx_storage.get("indication")
    with open('data/names_of_cities.txt', 'r', encoding='utf-8') as file:
        cities = [city.strip() for city in file]
        if city in cities:
            db_collection.insert_one({"_id": message.from_id, "city": city})
            keyboard = Keyboard().add(Text(label="Начать", payload={"cmd": "start"})).get_json()
            await message.answer("Ваш город успешно зарегистрирован!", keyboard=keyboard)
        else:
            keyboard = Keyboard().add(Text(label="Начать", payload={"cmd": "start"})).get_json()
            await message.answer("Некорректное название города", keyboard=keyboard)


#################################################################################################
# Меню
@bot.on.private_message(text="Меню")
@bot.on.private_message(payload={"cmd": "menu"})
async def menu_handler(message: Message):
    keyboard = (
        Keyboard(one_time=True).
        add(Text(label="Погода", payload={"cmd": "weather"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text(label="Валюта", payload={"cmd": "currency"}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text(label="Сменить город", payload={"cmd": "change_city"}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text(label="Назад", payload={"cmd": "start"}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer("Выбирай", keyboard=keyboard)


#####################################################################################################
# Обработка погоды
@bot.on.private_message(text="Погода")
@bot.on.private_message(payload={"cmd": "weather"})
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
@bot.on.private_message(text="Сегодня")
@bot.on.private_message(payload={"cmd": "weather_today"})
async def today_weather_handler(message: Message):
    user_id = message.from_id
    user_in_db = db_collection.find_one({'_id': user_id})
    if user_in_db:
        city = user_in_db.get('city')
        await message.answer(get_weather_forecast(city=city, day='today'))
    else:
        await message.answer("Произошла ошибка. Попробуйте сменить город.")


# Погода на завтра
@bot.on.private_message(text="Завтра")
@bot.on.private_message(payload={"cmd": "weather_tomorrow"})
async def tomorrow_weather_handler(message: Message):
    user_id = message.from_id
    user_in_db = db_collection.find_one({'_id': user_id})
    if user_in_db:
        city = user_in_db.get('city')
        await message.answer(get_weather_forecast(city=city, day='tomorrow'))
    else:
        await message.answer("Произошла ошибка. Попробуйте сменить город.")


################################################################################################
# Валюта
@bot.on.private_message(text="Валюта")
@bot.on.private_message(payload={"cmd": "currency"})
async def currency_handler(message: Message):
    keyboard = (
        Keyboard().add(Text(label="Назад", payload={"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer(exchange_rates, keyboard=keyboard)


#######################################################################################################
# Сменить город
@bot.on.private_message(text="Сменить город")
@bot.on.private_message(payload={"cmd": "change_city"})
async def change_city_handler(message: Message):
    await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
    await bot.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)


# Запуск бота
bot.run_forever()
