import requests

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "sparkline": False
}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", e)

    # Разбор ответа

# data = [
#     {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 'image': 'https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400', 'current_price': 76992, 'market_cap': 1548263910690, 'market_cap_rank': 1, 'fully_diluted_valuation': 1548263910690, 'total_volume': 27254862991, 'high_24h': 78120, 'low_24h': 76303, 'price_change_24h': -955.9500289027928, 'price_change_percentage_24h': -1.24482, 'market_cap_change_24h': -18906738411.239258, 'market_cap_change_percentage_24h': -1.20642, 'circulating_supply': 20105365.0, 'total_supply': 20105365.0, 'max_supply': 21000000.0, 'ath': 126080, 'ath_change_percentage': -38.93401, 'ath_date': '2025-10-06T10:57:42.000Z', 'atl': 67.81, 'atl_change_percentage': 113442.35203, 'atl_date': '2013-07-05T16:00:00.000Z', 'roi': None, 'last_updated': '2026-11-03T12:12:56.000Z'},
#     {'id': 'ethereum', 'symbol': 'eth', 'name': 'Ethereum', 'image': 'https://coin-images.coingecko.com/coins/images/279/large/ethereum.png?1696501628', 'current_price': 2264.19, 'market_cap': 276700170215, 'market_cap_rank': 2, 'fully_diluted_valuation': 276700170215, 'total_volume': 9110581865, 'high_24h': 2296.53, 'low_24h': 2235.31, 'price_change_24h': -26.742585179605612, 'price_change_percentage_24h': -1.18992, 'market_cap_change_24h': -3213184012.966614, 'market_cap_change_percentage_24h': -1.14792, 'circulating_supply': 122186161.86556138, 'total_supply': 122186161.86556138, 'max_supply': None, 'ath': 4946.05, 'ath_change_percentage': -54.22223, 'ath_date': '2025-08-24T11:21:03.000Z', 'atl': 0.432979, 'atl_change_percentage': 522833.27503, 'atl_date': '2015-10-19T16:00:00.000Z', 'roi': {'times': 43.309089628863546, 'currency': 'btc', 'percentage': 4330.908962886355}, 'last_updated': '2026-11-03T12:12:56.000Z'},
#     # сюда можно вставить остальные элементы списка...
# ]


def format_value(value):
    """Форматирует значение для красивого вывода."""
    if value is None:
        return "нет данных"
    if isinstance(value, float):
        # Округление до 4 знаков, но без лишних нулей, если это целое
        if value.is_integer():
            return str(int(value))
        return f"{value:.4f}"
    if isinstance(value, dict):
        # Для ROI выводим процент
        if 'percentage' in value:
            return f"{value['percentage']:.2f}%"
        return str(value)
    return str(value)

def print_crypto_info(crypto):
    name = crypto['name']
    print(f"{name} ({crypto['symbol'].upper()})")
 #   print(f"- ID: {crypto['id']}")
  #  print(f"- Символ: {crypto['symbol'].upper()}")
  #  print(f"- Название: {name}")
  #  print(f"- Изображение: {crypto['image']}")
    print(f"- Текущая цена: {format_value(crypto['current_price'])}")
    # print(f"- Рыночная капитализация: {format_value(crypto['market_cap'])}")
    # print(f"- Ранг по рыночной капитализации: {format_value(crypto['market_cap_rank'])}")
    # print(f"- Полностью разводнённая оценка: {format_value(crypto['fully_diluted_valuation'])}")
    # print(f"- Общий объём торгов: {format_value(crypto['total_volume'])}")
    # print(f"- Максимум за 24 ч: {format_value(crypto['high_24h'])}")
    # print(f"- Минимум за 24 ч: {format_value(crypto['low_24h'])}")
    #
    # change_val = crypto.get('price_change_24h')
    # change_pct = crypto.get('price_change_percentage_24h')
    # if change_val is not None and change_pct is not None:
    #     sign = "+" if change_val > 0 else ""
    #     print(f"- Изменение цены за 24 ч: {sign}{format_value(change_val)}")
    #     sign_pct = "+" if change_pct > 0 else ""
    #     print(f"- Изменение цены за 24 ч (%): {sign_pct}{format_value(change_pct)}%")
    # else:
    #     print("- Изменение цены за 24 ч: нет данных")
    #     print("- Изменение цены за 24 ч (%): нет данных")
    #
    # mc_change_val = crypto.get('market_cap_change_24h')
    # mc_change_pct = crypto.get('market_cap_change_percentage_24h')
    # if mc_change_val is not None and mc_change_pct is not None:
    #     sign = "+" if mc_change_val > 0 else ""
    #     print(f"- Изменение рыночной капитализации за 24 ч: {sign}{format_value(mc_change_val)}")
    #     sign_pct = "+" if mc_change_pct > 0 else ""
    #     print(f"- Изменение рыночной капитализации за 24 ч (%): {sign_pct}{format_value(mc_change_pct)}%")
    # else:
    #     print("- Изменение рыночной капитализации за 24 ч: нет данных")
    #     print("- Изменение рыночной капитализации за 24 ч (%): нет данных")
    #
    # print(f"- Оборотное предложение: {format_value(crypto['circulating_supply'])}")
    # print(f"- Общее предложение: {format_value(crypto['total_supply'])}")
    # max_supply = crypto.get('max_supply')
    # print(f"- Максимальное предложение: {format_value(max_supply)}")
    #
    # ath = crypto.get('ath')
    # ath_pct = crypto.get('ath_change_percentage')
    # ath_date = crypto.get('ath_date')
    # if ath is not None:
    #     print(f"- Исторический максимум (ATH): {format_value(ath)}")
    #     if ath_pct is not None:
    #         sign = "+" if ath_pct > 0 else ""
    #         print(f"- Изменение от ATH (%): {sign}{format_value(ath_pct)}%")
    #     if ath_date:
    #         date_str = ath_date.split('T')[0]
    #         print(f"- Дата ATH: {date_str}")
    #
    # atl = crypto.get('atl')
    # atl_pct = crypto.get('atl_change_percentage')
    # atl_date = crypto.get('atl_date')
    # if atl is not None:
    #     print(f"- Исторический минимум (ATL): {format_value(atl)}")
    #     if atl_pct is not None:
    #         sign = "+" if atl_pct > 0 else ""
    #         print(f"- Изменение от ATL (%): {sign}{format_value(atl_pct)}%")
    #     if atl_date:
    #         date_str = atl_date.split('T')[0]
    #         print(f"- Дата ATL: {date_str}")
    #
    # roi = crypto.get('roi')
    # if roi is not None and isinstance(roi, dict) and 'percentage' in roi:
    #     print(f"- ROI: {format_value(roi)} (в {roi.get('currency', 'USD')})")
    # elif roi is not None:
    #     print(f"- ROI: нет данных")
    # else:
    #     print("- ROI: нет данных")
    #
    # last_updated = crypto.get('last_updated')
    # if last_updated:
    #     date_str = last_updated.split('T')[0]
    #     print(f"- Последнее обновление: {date_str}")
    # else:
    #     print("- Последнее обновление: нет данных")


# Вывод информации по всем криптовалютам
for i, crypto in enumerate(data):
    print_crypto_info(crypto)
    if i < len(data) - 1:
        print("---")  # разделитель между монетами
