import asyncio
from config import api


async def get_names_of_cities() -> list:
    """ Получение названий городов из API-вк """
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
    """ Получение списка информации о городах """
    return asyncio.run(get_names_of_cities())


def write_cities_to_file(cities_name: list) -> None:
    """ Запись названия городов в файл """
    with open("../data/names_of_cities.txt", "w", encoding='utf-8') as file:
        for city in cities_name:
            file.write(str(city) + "\n")


if __name__ == '__main__':
    cities_name = get_cities()
    write_cities_to_file(cities_name=cities_name)
