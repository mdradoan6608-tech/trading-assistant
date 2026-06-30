import requests

from config.settings import FINNHUB_API_KEY
from core.response import success, error


BASE_URL = "https://finnhub.io/api/v1/quote"


def _quote(symbol):
    url = (
        f"{BASE_URL}?symbol={symbol}"
        f"&token={FINNHUB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")

    return response.json()


def get_price(symbol):
    symbol = symbol.upper()

    if not FINNHUB_API_KEY:
        return error("Finnhub API key not configured.")

    try:
        data = _quote(symbol)

        return success(
            f"Price for {symbol}",
            {
                "symbol": symbol,
                "price": data.get("c"),
                "high": data.get("h"),
                "low": data.get("l"),
                "open": data.get("o"),
                "previous_close": data.get("pc"),
            },
        )

    except Exception as e:
        return error(str(e))


def get_prices(symbols):
    if not FINNHUB_API_KEY:
        return error("Finnhub API key not configured.")

    result = []

    try:
        for symbol in symbols:
            symbol = symbol.upper()
            data = _quote(symbol)

            result.append({
                "symbol": symbol,
                "price": data.get("c"),
                "high": data.get("h"),
                "low": data.get("l"),
                "open": data.get("o"),
                "previous_close": data.get("pc"),
            })

        return success(
            "Watchlist prices",
            {"prices": result},
        )

    except Exception as e:
        return error(str(e))
