import os
from dotenv import load_dotenv
from vkbottle import EMPTY_KEYBOARD, BaseStateGroup, CtxStorage
from vkbottle.bot import Bot, Message
from loguru import logger
from database.db_connection import db_collection

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
    from_id = message.from_id
    existing_user = db_collection.find_one({"_id": from_id})
    if existing_user:
        await message.answer("Вы уже зарегистрирован в нашей системе.")
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


bot.run_forever()
