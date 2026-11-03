import requests

url = "https://api.coinlore.com/api/v1/coins/"
params = {"limit": 100}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", e)
    if "response" in locals():
        print("Статус код:", response.status_code)
        print("Текст ответа:", response.text)
