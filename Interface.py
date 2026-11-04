from datetime import datetime
import tkinter as tk
from tkinter import ttk
import requests


# --- Функция для форматирования даты ---
def format_last_updated(iso_string: str) -> str:
    """
    Преобразует ISO строку (2026-11-03T23:51:33.000Z) в формат:
    03-11-2026 в 23:51:33
    """
    try:
        # Убираем 'Z' (UTC) и парсим строку. Если есть миллисекунды (.000), strptime их съест с %f
        dt_obj = datetime.strptime(iso_string.replace('Z', ''), '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        # Если миллисекунд нет (редкий случай), пробуем без них
        try:
            dt_obj = datetime.strptime(iso_string.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
        except Exception:
            return iso_string  # Возвращаем как есть, если формат совсем неожиданный

    return dt_obj.strftime('%d-%m-%Y в %H:%M:%S')

print('Справочник текущих курсов криптовалют')
#main_cur = input('Введите целевую валюту (USD/EUR/RUB... :')

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": 'usd',
    #main_cur,
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "sparkline": False
}



try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    #print(data)
except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", e)
# data = [
#     {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 'current_price': 76992, 'market_cap': 1548263910690, 'market_cap_rank': 1, 'price_change_percentage_24h': -1.24482, 'last_updated': '2026-11-03T12:12:56.000Z'},
#     {'id': 'ethereum', 'symbol': 'eth', 'name': 'Ethereum', 'current_price': 2264.19, 'market_cap': 276700170215, 'market_cap_rank': 2, 'price_change_percentage_24h': -1.18992, 'last_updated': '2026-11-03T12:12:56.000Z'},
#     {'id': 'tether', 'symbol': 'usdt', 'name': 'Tether', 'current_price': 0.998634, 'market_cap': 178867203026, 'market_cap_rank': 3, 'price_change_percentage_24h': -0.04269, 'last_updated': '2026-11-03T12:12:56.000Z'},
#     # ... остальные элементы вашего списка
# ]


# Курсы фиатных валют к USD (примерные значения — при желании можно получать из API)
fiat_rates = {
    'usd': 1.0,
    'eur': 0.92,
    'rub': 181.5,
}

root = tk.Tk()
root.title("Курсы криптовалют")
root.geometry("420x300")

# --- Базовая валюта (крипта) ---
currencies = {coin['symbol']: coin for coin in data}
symbols = list(currencies.keys())

tk.Label(root, text='Базовая валюта (coin)').pack(pady=5)
base_combobox = ttk.Combobox(root, values=symbols, state='readonly')
base_combobox.pack(pady=3, padx=10)
base_combobox.current(0)

# --- Целевая валюта (в чём показываем цену) ---
target_currencies = list(fiat_rates.keys())
# если хотите целевой валютой тоже крипту, добавьте её символы в этот список

tk.Label(root, text='Целевая валюта').pack(pady=5)
target_combobox = ttk.Combobox(root, values=target_currencies, state='readonly')
target_combobox.pack(pady=3, padx=10)
target_combobox.current(0)

base_label = tk.Label(root, text='', justify='left', anchor='w')
base_label.pack(fill='x', padx=15, pady=8)

# --- Обработчик выбора ---
def update_base_label(event=None):
    base_sym = base_combobox.get()          # выбранная крипта
    target = target_combobox.get()          # выбранная целевая валюта

    coin = currencies[base_sym]
    rate = fiat_rates.get(target, 1.0)

    price = coin['current_price'] * rate    # цена в целевой валюте

    text = (
        f"{coin['name']} ({base_sym.upper()})\n"
        f"Цена: {price:,.2f} {target.upper()}\n"
        #f"Капитализация: {coin['market_cap'] * rate:,.0f} {target.upper()}\n"
        #f"Изменение за 24 ч: {coin['price_change_percentage_24h']} %\n"
        f"Обновлено: {format_last_updated(coin['last_updated'])}"
    )
    base_label.config(text=text)

base_combobox.bind('<<ComboboxSelected>>', update_base_label)
target_combobox.bind('<<ComboboxSelected>>', update_base_label)  # тот же обработчик
update_base_label()

root.mainloop()
