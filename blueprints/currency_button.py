from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from utils.currency import exchange_rates

bp = Blueprint()
bp.on.vbml_ignore_case = True


# Обработка кнопки "Валюта"
@bp.on.private_message(text="Валюта")
@bp.on.private_message(payload={"cmd": "currency"})
async def currency_handler(message: Message):
    keyboard = (
        Keyboard().add(Text(label="Назад", payload={"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer(exchange_rates, keyboard=keyboard)
