from vkbottle.bot import Blueprint, Message
from vkbottle import BaseStateGroup, CtxStorage, Keyboard, Text, EMPTY_KEYBOARD

from database.db_connection import db_collection

bp = Blueprint()
bp.on.vbml_ignore_case = True
ctx_storage = CtxStorage()


# Регистрация города
class CityState(BaseStateGroup):
    """ Сохранение стейтов для регистрации города """
    CITY_CONFIRMATION = 'CITY_CONFIRMATION'
    CITY_INDICATION = 'CITY_INDICATION'


# Получить город из профиля
async def get_city_handler(message: Message):
    user_info = await bp.api.users.get(user_ids=message.from_id, fields=['city'])
    if user_info[0].city:
        city = user_info[0].city.title
        ctx_storage.set("city", city)
        await message.answer(f"Ваш город {city}?", keyboard=EMPTY_KEYBOARD)
        await bp.state_dispenser.set(message.peer_id, CityState.CITY_CONFIRMATION)
    else:
        await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
        await bp.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)


# Обновление города или его регистрация
async def city_update_or_registration_handler(message: Message):
    city_name = ctx_storage.get("city")
    existing_user = db_collection.find_one({"_id": message.from_id})
    if existing_user:
        db_collection.update_one({"_id": message.from_id}, {"$set": {"city": city_name}})
    else:
        db_collection.insert_one({"_id": message.from_id, "city": city_name})
    keyboard = Keyboard().add(Text(label="Начать", payload={"cmd": "start"})).get_json()
    await message.answer("Ваш город успешно зарегистрирован!", keyboard=keyboard)
    await bp.state_dispenser.delete(message.peer_id)


# Подтверждение города
@bp.on.private_message(state=CityState.CITY_CONFIRMATION)
async def city_confirmation_handler(message: Message):
    ctx_storage.set("confirmation", message.text)
    confirmation = ctx_storage.get("confirmation").lower()
    if confirmation == "да":
        await city_update_or_registration_handler(message=message)
    elif confirmation == "нет":
        await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
        await bp.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)
    else:
        await message.answer('Пожалуйста, напишите "Да" или "Нет"')


# Проверка города, указанного пользователем
@bp.on.private_message(state=CityState.CITY_INDICATION)
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
            await bp.state_dispenser.delete(message.peer_id)
        else:
            keyboard = Keyboard().add(Text(label="Начать", payload={"cmd": "start"})).get_json()
            await message.answer("Некорректное название города", keyboard=keyboard)
            await bp.state_dispenser.delete(message.peer_id)
