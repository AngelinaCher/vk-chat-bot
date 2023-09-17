from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

bp = Blueprint()
bp.on.vbml_ignore_case = True


@bp.on.private_message(text="Меню")
@bp.on.private_message(payload={"cmd": "menu"})
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
