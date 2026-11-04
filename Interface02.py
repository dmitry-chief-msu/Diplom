import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests

# Целевые валюты (полный список CoinGecko)
# Код валюты -> русское название (для отображения в комбобоксе)
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

TARGET_CURRENCIES = list(TARGET_CURRENCY_NAMES.keys())  # коды для API

def currency_display(code: str) -> str:
    return f"{TARGET_CURRENCY_NAMES[code]} ({code.upper()})"

# Для комбобокса: "Доллар США - USD", "Евро - EUR", ...
target_display_values = [currency_display(code) for code in TARGET_CURRENCIES]
# Обратное соответствие: "Доллар США - USD" -> "usd"
display_to_currency = {currency_display(code): code for code in TARGET_CURRENCIES}



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



# Словарь: symbol -> coin
currencies = {coin['symbol']: coin for coin in data}

# Список для комбобокса: "Bitcoin (BTC)", "Ethereum (ETH)", ...
combo_display_values = [f"{coin['name']} ({coin['symbol'].upper()})" for coin in data]
# Обратное соответствие: "Bitcoin (BTC)" -> "btc"
display_to_symbol = {f"{coin['name']} ({coin['symbol'].upper()})": coin['symbol'] for coin in data}


# --- Форматирование цены ---
def format_price(value) -> str:
    if value is None:
        return '—'
    if value >= 1:
        return f"{value:,.2f}"
    return f"{value:,.8f}".rstrip('0').rstrip('.')

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
root.geometry("440x440")

tk.Label(root, text='Базовая валюта (coin)', font=('Arial', 11, 'bold')).pack(pady=5)
base_combobox = ttk.Combobox(root, values=combo_display_values, state='readonly', width = 55)
base_combobox.pack(pady=3, padx=10)
base_combobox.current(0)

tk.Label(root, text='Целевая валюта', font=('Arial', 11, 'bold')).pack(pady=5)
target_combobox = ttk.Combobox(root, values=target_display_values, state='readonly', width = 35)
target_combobox.pack(pady=3, padx=10)
target_combobox.current(TARGET_CURRENCIES.index('usd'))  # по умолчанию USD


# --- Рамка «Курс в выбранной валюте» ---
course_frame = tk.LabelFrame(root, text="Курс в выбранной валюте",
                             font=('Arial', 11, 'bold'), fg='#333333',
                             bd=2, relief='groove', bg='#f5f5f7')
course_frame.pack(fill='x', padx=15, pady=10)

info_label = tk.Label(course_frame, text='', justify='left', anchor='w', bg='#f5f5f7')
info_label.pack(fill='x', padx=10, pady=8)

# --- Рамка «Котировки в основных валютах» ---
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


# # --- Блок «Котировки в основных валютах» ---
# prices_frame = tk.Frame(root, bd=2, relief='groove', bg='#f5f5f7')
# prices_frame.pack(fill='x', padx=15, pady=10)
#
# # Заголовок внутри рамки
# header_label = tk.Label(prices_frame, text="Котировки в основных валютах",
#                         font=('Arial', 11, 'bold'), bg='#f5f5f7', fg='#333333')
# header_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=(10, 5))
#
# # Три поля цен
# price_usd_label = tk.Label(prices_frame, text='Цена (USD): —', anchor='w', bg='#f5f5f7')
# price_eur_label = tk.Label(prices_frame, text='Цена (EUR): —', anchor='w', bg='#f5f5f7')
# price_rub_label = tk.Label(prices_frame, text='Цена (RUB): —', anchor='w', bg='#f5f5f7')
#
# # Равномерное распределение колонок
# prices_frame.columnconfigure((0, 1, 2), weight=1, uniform='price_cols')
#
# price_usd_label.grid(row=1, column=0, sticky='ew', padx=(10, 5), pady=5)
# price_eur_label.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
# price_rub_label.grid(row=1, column=2, sticky='ew', padx=(5, 10), pady=5)

status_label = tk.Label(root, text='', fg='gray')
status_label.pack()

# Кэш последних полученных курсов (чтобы GUI не «падал» при сетевой ошибке)
prices_cache = {}

def update_info(event=None, refresh=False):
    #base_sym = base_combobox.get()

    # Получаем отображаемую строку, например "Bitcoin (BTC)"
    display_text = base_combobox.get()

    # По ней находим символ монеты: "Bitcoin (BTC)" → "btc"
    base_sym = display_to_symbol.get(display_text)
    if base_sym is None:
        # На всякий случай: если что-то пошло не так, пробуем взять первый элемент
        base_sym = list(currencies.keys())[0]

    #target = target_combobox.get()

    target_display = target_combobox.get()          # "Доллар США - USD"
    target = display_to_currency.get(target_display)  # "usd"
    if target is None:                              # защита от рассинхрона
        target = 'usd'

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

# --- Три фиксированных поля: USD / EUR / RUB (не зависят от комбобокса) ---
    price_usd_label.config(text=f"Цена (USD): {format_price(prices.get('usd'))}")
    price_eur_label.config(text=f"Цена (EUR): {format_price(prices.get('eur'))}")
    price_rub_label.config(text=f"Цена (RUB): {format_price(prices.get('rub'))}")


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
