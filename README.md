# vk-chat-bot
Тестовое задание: Чат-бот на платформе VK

## Описание

Данный проект - это выполнение тестового задания. [Ссылка]([https://github.com/AngelinaCher/R4C/blob/master/tasks.md](https://docs.google.com/document/d/1mEiSQT2AK1BWNad7dyuNgVZ02R1nyHm0YeyiaBjnQNM/edit)https://docs.google.com/document/d/1mEiSQT2AK1BWNad7dyuNgVZ02R1nyHm0YeyiaBjnQNM/edit)
на задание. Платформа: ВК.
Прогноз погоды и показ курса валют реализован с помощью открытых API. 


## Установка

1. Склонируйте репозиторий: `git clone https://github.com/AngelinaCher/vk-chat-bot.git `
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте виртуальное окружение:
    * Для Windows: `venv\Scripts\activate`
    * Для Linux: `source venv/bin/activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Запуск бота: 
```python bot.py```

### Установка с использованием Poetry

1. Склонируйте репозиторий: `git clone https://github.com/AngelinaCher/vk-chat-bot.git `
2. Перейдите в директорию проекта `cd R4C`
3. Активируйте виртуальное окружение: `poetry shell`
4. Установите зависимости с помощью Poetry: `poetry install`
5. Запуск бота: 
```python bot.py```

## Использование

* Регистрация города пользователя
* Запрос прогноза погоды
* Запрос курса валют
* Смена города

## Технологии
* Python 3.10.12
* vkbottle 4.3.12
* MongoDB
* pymongo 4.5.0

## Структура проекта
* [blueprints](blueprints) - бизнес-логика бота
   + [change_city_button.py](blueprints%2Fchange_city_button.py) - логика кнопки "Сменить город"
   + [change_city_button.py](blueprints%2Fchange_city_button.py) - логика регистрации города
   + [currency_button.py](blueprints%2Fcurrency_button.py) - логика кнопки "Валюта"
   + [menu_button.py](blueprints%2Fmenu_button.py) - логика кнопки "Меню"
   + [menu_button.py](blueprints%2Fmenu_button.py) - логика кнопки "Начать"
   + [menu_button.py](blueprints%2Fmenu_button.py) - логика кнопки "Прогноз погоды"
* [data](data) - хранения различных данных
   + [names_of_cities.txt](data%2Fnames_of_cities.txt) - название город, взятых из VK-API
* [database](database) - работа с БД
   + [db_connection.py](database%2Fdb_connection.py) - подключение к БД
* [utils](utils) - утилиты
   + [currency.py](utils%2Fcurrency.py) - логика отображения курса валют
   + [names_of_cities.py](utils%2Fnames_of_cities.py) - логика формирование списка название городов из VK-API
   + [weather.py](utils%2Fweather.py) - логика отображения прогноза погоды
* [.env.template](.env.template) - шаблон для переменных окружения
* [bot.py](bot.py) - запуск программы
* [requirements.txt](requirements.txt) - файл зависимостей