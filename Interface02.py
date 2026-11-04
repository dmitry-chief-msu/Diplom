import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests

# --- Целевые валюты (полный список CoinGecko) ---
TARGET_CURRENCIES = [
#    "btc", "eth", "ltc", "bch", "bnb", "eos", "xrp", "xlm", "link", "dot",
#    "yfi", "sol",
    "usd", "eur", "rub", "cny", "aed", "ars", "aud", "bdt", "bhd", "bmd",
    "brl", "cad", "chf", "clp", "czk", "dkk", "gbp", "gel", "hkd",
    "huf", "idr", "ils", "inr", "jpy", "krw", "kwd", "lkr", "mmk", "mxn",
    "myr", "ngn", "nok", "nzd", "php", "pkr", "pln", "sar", "sek",
    "sgd", "thb", "try", "twd", "uah", "vef", "vnd", "zar", "xdr", "xag",
    "xau", "bits", "sats"
]

API_URL = "https://api.coingecko.com/api/v3"


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


# # Данные по монетам (здесь — сокращённо; у вас они получаются из /coins/markets)
# data = [
#     {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 'current_price': 76992,
#      'market_cap': 1548263910690, 'price_change_percentage_24h': -1.24482,
#      'last_updated': '2026-11-03T12:12:56.000Z'},
#     {'id': 'ethereum', 'symbol': 'eth', 'name': 'Ethereum', 'current_price': 2264.19,
#      'market_cap': 276700170215, 'price_change_percentage_24h': -1.18992,
#      'last_updated': '2026-11-03T12:12:56.000Z'},
#     {'id': 'tether', 'symbol': 'usdt', 'name': 'Tether', 'current_price': 0.998634,
#      'market_cap': 178867203026, 'price_change_percentage_24h': -0.04269,
#      'last_updated': '2026-11-03T12:12:56.000Z'},
# ]

currencies = {coin['symbol']: coin for coin in data}

# --- Форматирование даты ---
def format_last_updated(iso_string: str) -> str:
    try:
        dt_obj = datetime.strptime(iso_string.replace('Z', ''), '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        try:
            dt_obj = datetime.strptime(iso_string.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
        except Exception:
            return iso_string
    return dt_obj.strftime('%d-%m-%Y в %H:%M:%S')

# --- Запрос реальных курсов у биржи (CoinGecko) ---
def fetch_prices_for_coin(coin_id: str) -> dict:
    """
    Возвращает словарь {'usd': 76992, 'eur': 70800, 'btc': 1.0, ...}
    для одной монеты сразу во всех целевых валютах.
    """
    params = {
        'ids': coin_id,
        'vs_currencies': ','.join(TARGET_CURRENCIES),   # все валюты одним запросом
    }
    response = requests.get(f"{API_URL}/simple/price", params=params, timeout=10)
    response.raise_for_status()
    result = response.json()

    if coin_id not in result:
        raise ValueError(f"Монета '{coin_id}' не найдена в ответе API")

    return result[coin_id]   # {'usd': 76992, 'rub': ..., 'btc': 1.0, ...}

# --- GUI ---
root = tk.Tk()
root.title("Курсы криптовалют")
root.geometry("440x360")

tk.Label(root, text='Базовая валюта (coin)').pack(pady=5)
base_combobox = ttk.Combobox(root, values=list(currencies.keys()), state='readonly')
base_combobox.pack(pady=3, padx=10)
base_combobox.current(0)

tk.Label(root, text='Целевая валюта').pack(pady=5)
target_combobox = ttk.Combobox(root, values=TARGET_CURRENCIES, state='readonly')
target_combobox.pack(pady=3, padx=10)
target_combobox.set('usd')

info_label = tk.Label(root, text='', justify='left', anchor='w')
info_label.pack(fill='x', padx=15, pady=8)

status_label = tk.Label(root, text='', fg='gray')
status_label.pack()

# Кэш последних полученных курсов (чтобы GUI не «падал» при сетевой ошибке)
prices_cache = {}

def update_info(event=None, refresh=False):
    base_sym = base_combobox.get()
    target = target_combobox.get()
    coin = currencies[base_sym]

    prices = prices_cache.get(coin['id'])

    # Запрашиваем реальные курсы, если их ещё нет или нажали "Обновить"
    if prices is None or refresh:
        try:
            prices = fetch_prices_for_coin(coin['id'])
            prices_cache[coin['id']] = prices
            status_label.config(text=f'Курсы получены: {datetime.now().strftime("%H:%M:%S")} (локальное время)',
                                fg='green')
        except (requests.exceptions.RequestException, ValueError) as e:
            status_label.config(text=f'Ошибка сети: {e}. Показаны кэшированные данные',
                                fg='red')

    if prices is None:
        info_label.config(text='Нет данных — проверьте подключение к интернету')
        return

    price = prices.get(target)
    price_text = f"{price:,.6f}".rstrip('0').rstrip('.') if price is not None else 'нет данных'

    text = (
        f"{coin['name']} ({base_sym.upper()})\n"
        f"Цена: {price_text} {target.upper()}\n"
        f"\n"
        #f"Изменение за 24 ч: {coin['price_change_percentage_24h']} %\n"
        f"Обновлено {format_last_updated(coin['last_updated'])} UTC"
    )
    info_label.config(text=text)

ttk.Button(root, text='Обновить курсы', command=lambda: update_info(refresh=True)).pack(pady=6)

base_combobox.bind('<<ComboboxSelected>>', update_info)
target_combobox.bind('<<ComboboxSelected>>', update_info)
update_info()

root.mainloop()
