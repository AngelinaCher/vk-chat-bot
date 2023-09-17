import os
from dotenv import load_dotenv
from vkbottle import load_blueprints_from_package
from vkbottle.bot import Bot, Message

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

for bp in load_blueprints_from_package("blueprints"):
    bp.load(bot)

# Запуск бота
bot.run_forever()
