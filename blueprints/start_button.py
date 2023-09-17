from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from database.db_connection import db_collection
from blueprints.city import get_city_handler

bp = Blueprint()
bp.on.vbml_ignore_case = True


# Обработка кнопки "Начать"
@bp.on.private_message(lev="Начать")
@bp.on.private_message(payload={"cmd": "start"})
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
