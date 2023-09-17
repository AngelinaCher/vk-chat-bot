from vkbottle.bot import Blueprint, Message
from vkbottle import EMPTY_KEYBOARD

from blueprints.city import CityState

bp = Blueprint()
bp.on.vbml_ignore_case = True


# Сменить город
@bp.on.private_message(text="Сменить город")
@bp.on.private_message(payload={"cmd": "change_city"})
async def change_city_handler(message: Message):
    await message.answer("Пожалуйста, укажите свой город", keyboard=EMPTY_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, CityState.CITY_INDICATION)
