import os
from dotenv import load_dotenv
from vkbottle import EMPTY_KEYBOARD, BaseStateGroup, CtxStorage, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message
from loguru import logger
from database.db_connection import db_collection
from weather import get_weather_forecast

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


# обработка кнопки "Начать"
@bot.on.private_message(lev="Начать")
async def get_city_handler(message: Message):
    existing_user = db_collection.find_one({"_id": message.from_id})
    if existing_user:
        keyboard = Keyboard(one_time=True).add(Text(label="Меню", payload={"cmd": "menu"}))
        await message.answer('Вы зарегистрированы. Введите "Меню" или нажмите на кнопку.', keyboard=keyboard)
    else:
        user_info = await bot.api.users.get(user_ids=message.from_id, fields=['city'])
        if user_info[0].city:
            city = user_info[0].city.title
            ctx_storage.set("city", city)
            await message.answer(f"Ваш город {city}?", keyboard=EMPTY_KEYBOARD)
            await bot.state_dispenser.set(message.peer_id, CityState.CITY_CONFIRMATION)
        else:
            await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
            await bot.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)


# подтверждение города
@bot.on.private_message(state=CityState.CITY_CONFIRMATION)
async def city_confirmation_handler(message: Message):
    ctx_storage.set("confirmation", message.text)
    confirmation = ctx_storage.get("confirmation").lower()
    if confirmation == "да":
        city_name = ctx_storage.get("city")
        db_collection.insert_one({"_id": message.from_id, "city": city_name})
        await message.answer("Ваш город успешно зарегистрирован!", keyboard=EMPTY_KEYBOARD)
    elif confirmation == "нет":
        await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
        await bot.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)
    else:
        await message.answer('Пожалуйста, напишите "Да" или "Нет"', keyboard=EMPTY_KEYBOARD)


# проверка города, указанного пользователем
@bot.on.private_message(state=CityState.CITY_INDICATION)
async def city_indication_handler(message: Message):
    ctx_storage.set("indication", message.text.capitalize())
    city = ctx_storage.get("indication")
    with open('data/names_of_cities.txt', 'r', encoding='utf-8') as file:
        cities = [city.strip() for city in file]
        if city in cities:
            db_collection.insert_one({"_id": message.from_id, "city": city})
            await message.answer("Ваш город успешно зарегистрирован!", keyboard=EMPTY_KEYBOARD)
        else:
            await message.answer("Некорректное название города", keyboard=EMPTY_KEYBOARD)


@bot.on.private_message(text="Меню")
@bot.on.private_message(payload={"cmd": "menu"})
async def menu_handler(message: Message):
    keyboard = (
        Keyboard(one_time=True).
        add(Text(label="Погода", payload={"cmd": "weather"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Пробки"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Афиша"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Валюта"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Сменить город"), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer("Выбирай", keyboard=keyboard)


# Обработка погоды
@bot.on.private_message(text="Погода")
@bot.on.private_message(payload={"cmd": "weather"})
async def weather_handler(message: Message):
    keyboard = (
        Keyboard()
        .add(Text(label="Сегодня", payload={"cmd": "weather_today"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(label="Завтра", payload={"cmd": "weather_tomorrow"}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer("Погода на сегодня или завтра?", keyboard=keyboard)


# Погода на сегодня
@bot.on.private_message(text="Сегодня")
@bot.on.private_message(payload={"cmd": "weather_today"})
async def today_weather_handler(message: Message):
    await message.answer(get_weather_forecast(city='москва', day='today'))


# Погода на завтра
@bot.on.private_message(text="Завтра")
@bot.on.private_message(payload={"cmd": "weather_tomorrow"})
async def tomorrow_weather_handler(message: Message):
    await message.answer(get_weather_forecast(city='москва', day='tomorrow'))


bot.run_forever()
