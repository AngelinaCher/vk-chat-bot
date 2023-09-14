import os
from dotenv import load_dotenv
from vkbottle import EMPTY_KEYBOARD, BaseStateGroup, CtxStorage, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message
from loguru import logger

# отключение логгера
logger.disable('vkbottle')
load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)


@bot.on.private_message(text="Действие")
async def menu_handler(message: Message):
    keyboard = (
        Keyboard().
        add(Text("Погода"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Пробки"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Афиша"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Валюта"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Сменить город"), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer("Keyboard", keyboard=keyboard)
