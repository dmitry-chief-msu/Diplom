import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests

# ---------- КОНСТАНТЫ И СЛОВАРИ ----------

TARGET_CURRENCY_NAMES = {
    "usd": "Доллар США",
    "eur": "Евро",
    "rub": "Российский рубль",
    "cny": "Китайский юань",
    "aed": "Дирхам ОАЭ",
    "ars": "Аргентинское песо",
    "aud": "Австралийский доллар",
    "bdt": "Бангладешская така",
    "bhd": "Бахрейнский динар",
    "bmd": "Бермудский доллар",
    "brl": "Бразильский реал",
    "cad": "Канадский доллар",
    "chf": "Швейцарский франк",
    "clp": "Чилийское песо",
    "czk": "Чешская крона",
    "dkk": "Датская крона",
    "gbp": "Британский фунт",
    "gel": "Грузинский лари",
    "hkd": "Гонконгский доллар",
    "huf": "Венгерский форинт",
    "idr": "Индонезийская рупия",
    "ils": "Израильский шекель",
    "inr": "Индийская рупия",
    "jpy": "Японская иена",
    "krw": "Южнокорейская вона",
    "kwd": "Кувейтский динар",
    "lkr": "Шри-ланкийская рупия",
    "mmk": "Мьянманский кьят",
    "mxn": "Мексиканское песо",
    "myr": "Малайзийский ринггит",
    "ngn": "Нигерийская найра",
    "nok": "Норвежская крона",
    "nzd": "Новозеландский доллар",
    "php": "Филиппинское песо",
    "pkr": "Пакистанская рупия",
    "pln": "Польский злотый",
    "sar": "Саудовский риял",
    "sek": "Шведская крона",
    "sgd": "Сингапурский доллар",
    "thb": "Тайский бат",
    "try": "Турецкая лира",
    "twd": "Тайваньский доллар",
    "uah": "Украинская гривна",
    "vef": "Венесуэльский боливар",
    "vnd": "Вьетнамский донг",
    "zar": "Южноафриканский ранд",
    "xdr": "СПЗ (валютная корзина МВФ)",
    "xag": "Серебро (унция)",
    "xau": "Золото (унция)",
    "bits": "Биты (микробиткоин)",
    "sats": "Сатоши",
}
TARGET_CURRENCIES = list(TARGET_CURRENCY_NAMES.keys())

API_URL = "https://api.coingecko.com/api/v3"

# ---------- ЗАПРОСЫ К API ----------

def fetch_coins() -> list:
    """Топ-100 монет с метаданными (цена — только в USD)."""
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(f"{API_URL}/coins/markets", params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_all_prices(coin_ids: list) -> dict:
    """
    Цены ВСЕХ монет сразу во всех целевых валютах — ОДНИМ запросом.
    Возвращает {coin_id: {'usd': ..., 'eur': ..., 'rub': ...}, ...}
    """
    params = {
        "ids": ",".join(coin_ids),
        "vs_currencies": ",".join(TARGET_CURRENCIES),
    }
    response = requests.get(f"{API_URL}/simple/price", params=params, timeout=15)
    response.raise_for_status()
    return response.json()

# ---------- ФОРМАТИРОВАНИЕ ----------

def currency_display(code: str) -> str:
    return f"{TARGET_CURRENCY_NAMES[code]} ({code.upper()})"

target_display_values = [currency_display(code) for code in TARGET_CURRENCIES]
display_to_currency = {currency_display(code): code for code in TARGET_CURRENCIES}

def format_price(value) -> str:
    if value is None:
        return '—'
    if value >= 1:
        return f"{value:,.2f}"
    return f"{value:,.8f}".rstrip('0').rstrip('.')

def format_last_updated(iso_string: str) -> str:
    try:
        dt_obj = datetime.strptime(iso_string.replace('Z', ''), '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        try:
            dt_obj = datetime.strptime(iso_string.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
        except Exception:
            return iso_string
    return dt_obj.strftime('%d-%m-%Y в %H:%M:%S')

# ---------- ЗАГРУЗКА ДАННЫХ ПРИ СТАРТЕ ----------

coins = []
currencies = {}
display_to_symbol = {}
combo_display_values = []
prices_cache = {}   # {coin_id: {'usd': ..., 'eur': ..., ...}}

def load_all(refresh=False):
    """Загружает (или обновляет) список монет и цены всех монет одним запросом."""
    global coins, currencies, display_to_symbol, combo_display_values

    new_coins = fetch_coins()
    new_prices = fetch_all_prices([coin['id'] for coin in new_coins])

    coins = new_coins
    currencies = {coin['symbol']: coin for coin in coins}
    combo_display_values = [f"{coin['name']} ({coin['symbol'].upper()})" for coin in coins]
    display_to_symbol = {f"{coin['name']} ({coin['symbol'].upper()})": coin['symbol'] for coin in coins}

    for coin_id, prices in new_prices.items():
        prices_cache[coin_id] = prices

    if not refresh:
        base_combobox['values'] = combo_display_values
        base_combobox.current(0)

# ---------- GUI ----------

root = tk.Tk()
root.title("Курсы криптовалют")
root.geometry("440x440")

tk.Label(root, text='Базовая валюта (coin)', font=('Arial', 11, 'bold')).pack(pady=5)
base_combobox = ttk.Combobox(root, values=[], state='readonly', width=55)
base_combobox.pack(pady=3, padx=10)

tk.Label(root, text='Целевая валюта', font=('Arial', 11, 'bold')).pack(pady=5)
target_combobox = ttk.Combobox(root, values=target_display_values, state='readonly', width=35)
target_combobox.pack(pady=3, padx=10)
target_combobox.current(TARGET_CURRENCIES.index('usd'))

course_frame = tk.LabelFrame(root, text="Курс в выбранной валюте",
                             font=('Arial', 11, 'bold'), fg='#333333',
                             bd=2, relief='groove', bg='#f5f5f7')
course_frame.pack(fill='x', padx=15, pady=10)

info_label = tk.Label(course_frame, text='', justify='left', anchor='w', bg='#f5f5f7')
info_label.pack(fill='x', padx=10, pady=8)

prices_frame = tk.LabelFrame(root, text="Котировки в основных валютах",
                             font=('Arial', 11, 'bold'), fg='#333333',
                             bd=2, relief='groove', bg='#f5f5f7')
prices_frame.pack(fill='x', padx=15, pady=10)

price_usd_label = tk.Label(prices_frame, text='Цена (USD): —', anchor='w', bg='#f5f5f7')
price_eur_label = tk.Label(prices_frame, text='Цена (EUR): —', anchor='w', bg='#f5f5f7')
price_rub_label = tk.Label(prices_frame, text='Цена (RUB): —', anchor='w', bg='#f5f5f7')

prices_frame.columnconfigure((0, 1, 2), weight=1, uniform='price_cols')
price_usd_label.grid(row=0, column=0, sticky='ew', padx=(10, 5), pady=8)
price_eur_label.grid(row=0, column=1, sticky='ew', padx=5, pady=8)
price_rub_label.grid(row=0, column=2, sticky='ew', padx=(5, 10), pady=8)

status_label = tk.Label(root, text='', fg='gray')
status_label.pack()

# ---------- ЛОГИКА ОБНОВЛЕНИЯ ----------

def update_info(event=None):
    base_sym = display_to_symbol.get(base_combobox.get())
    if base_sym is None:
        base_sym = list(currencies.keys())[0]

    target = display_to_currency.get(target_combobox.get())
    if target is None:
        target = 'usd'

    coin = currencies[base_sym]
    prices = prices_cache.get(coin['id'])

    if prices is None:
        # Цены этой монеты нет в кэше (например, монета добавилась после загрузки)
        try:
            prices_cache.update(fetch_all_prices([coin['id']]))
            prices = prices_cache.get(coin['id'])
            status_label.config(
                text=f'Курсы получены: {datetime.now().strftime("%H:%M:%S")} (локальное время)',
                fg='green')
        except requests.exceptions.RequestException as e:
            status_label.config(text=f'Ошибка сети: {e}. Показаны кэшированные данные', fg='red')
            return

    price_usd_label.config(text=f"Цена (USD): {format_price(prices.get('usd'))}")
    price_eur_label.config(text=f"Цена (EUR): {format_price(prices.get('eur'))}")
    price_rub_label.config(text=f"Цена (RUB): {format_price(prices.get('rub'))}")

    price = prices.get(target)
    price_text = format_price(price) if price is not None else 'нет данных'

    text = (
        f"{coin['name']} ({base_sym.upper()})\n"
        f"Цена: {price_text} {target.upper()}\n"
        f"\n"
        f"Обновлено {format_last_updated(coin['last_updated'])} UTC"
    )
    info_label.config(text=text)

def refresh_all():
    """Полное обновление: список монет + цены всех монет."""
    try:
        load_all(refresh=True)
        status_label.config(
            text=f'Данные обновлены: {datetime.now().strftime("%H:%M:%S")} (локальное время)',
            fg='green')
        update_info()
    except requests.exceptions.RequestException as e:
        status_label.config(text=f'Ошибка сети: {e}. Показаны предыдущие данные', fg='red')

# Загрузка при старте
try:
    load_all()
    status_label.config(text='Данные загружены', fg='green')
except requests.exceptions.RequestException as e:
    status_label.config(text=f'Ошибка сети при старте: {e}', fg='red')

ttk.Button(root, text='Обновить курсы', command=refresh_all).pack(pady=6)

base_combobox.bind('<<ComboboxSelected>>', update_info)
target_combobox.bind('<<ComboboxSelected>>', update_info)
update_info()

root.mainloop()
