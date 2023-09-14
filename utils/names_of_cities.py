import os
import asyncio
from vkbottle.api import API
from dotenv import load_dotenv

load_dotenv()

api = API(os.getenv("USER_ACCESS_TOKEN"))


async def get_names_of_cities() -> list:
    all_name_cities = []
    countries = await api.database.get_countries(
        need_all=True,
        code='RU,UA,BY,AZ,AM,DE,GE,DK,IL,ES,IT,KZ,CA,MX,MN,NL,AE,PL,RS,TJ,TH,TW,TM,TR,UZ,FI,ME,CZ,CH,SE,EE,KR,JP'
    )
    countries_id = [country.id for country in countries.items]
    for country_id in countries_id:
        cities = await api.database.get_cities(country_id=country_id)
        cities_title = [city.title for city in cities.items]
        all_name_cities.extend(cities_title)
    return all_name_cities


def get_cities() -> list:
    return asyncio.run(get_names_of_cities())


def write_cities_to_file(cities_name: list) -> None:
    with open("../data/names_of_cities.txt", "w", encoding='utf-8') as file:
        for city in cities_name:
            file.write(str(city) + "\n")


if __name__ == '__main__':
    cities_name = get_cities()
    write_cities_to_file(cities_name=cities_name)
