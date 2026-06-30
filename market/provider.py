import requests

from config.settings import FINNHUB_API_KEY
from core.response import success, error


def get_price(symbol):
    symbol = symbol.upper()

    if not FINNHUB_API_KEY:
        return error("Finnhub API key not configured.")

    url = (
        "https://finnhub.io/api/v1/quote"
        f"?symbol={symbol}"
        f"&token={FINNHUB_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return error(f"HTTP {response.status_code}")

        data = response.json()

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
