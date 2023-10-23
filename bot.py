from vkbottle import load_blueprints_from_package
from vkbottle.bot import Bot
from config import TOKEN


def main():
    bot = Bot(token=TOKEN)
    for bp in load_blueprints_from_package("blueprints"):
        bp.load(bot)
    # Запуск бота
    bot.run_forever()


if __name__ == '__main__':
    main()
