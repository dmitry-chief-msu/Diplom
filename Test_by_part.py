import requests

api_url = "https://api.coingecko.com/api/v3"
def fetch_coins() -> list:
    """ТОП-100 КРИПТОВАЛЮТ ДЛЯ ВНЕСЕНИЯ В КОМБОБОКС"""
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1, #Выбираем первую сотню криптовалют
        "sparkline": False,
    }
    response = requests.get(f"{api_url}/coins/markets", params=params, timeout=10)
    response.raise_for_status()
    return response.json()

test = fetch_coins()
print(test)
