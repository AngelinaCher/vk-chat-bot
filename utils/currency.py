import requests

url_currency = 'https://www.cbr-xml-daily.ru/daily_json.js'


# Возвращает строку с курсом валют по отношению к рублю
def get_exchange_rate(url: str, currencies: dict) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        result = ""
        data = response.json()
        valute = data.get("Valute")
        for code, symbol in currencies.items():
            char_code = valute[code].get("CharCode")
            name = valute[code].get("Name")
            value = valute[code].get("Value")
            result += f"{name} ({char_code}) 1{symbol} = {round(value, 2)} ₽\n"
        return result
    else:
        return "Произошла ошибка"


code_of_currencies = ["USD", "EUR", "CNY", "GBP", "CHF"]
currency_symbol = ["$", "€", "¥", "£", "₣"]
code_and_symbol = dict(zip(code_of_currencies, currency_symbol))
exchange_rates = get_exchange_rate(url=url_currency, currencies=code_and_symbol)
