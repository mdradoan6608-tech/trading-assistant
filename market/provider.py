import requests

from config.settings import FINNHUB_API_KEY
from core.response import success, error
from utils.logger import logger


BASE_URL = "https://finnhub.io/api/v1/quote"

FRIENDLY_ERROR = "Price service is temporarily unavailable. Please try again in a few minutes."


def _quote(symbol):
    url = (
        f"{BASE_URL}?symbol={symbol}"
        f"&token={FINNHUB_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")

    return response.json()


def _friendly_error(e, symbol=""):
    logger.error(f"Finnhub error for {symbol}: {e}")

    if isinstance(e, requests.exceptions.Timeout):
        return FRIENDLY_ERROR
    if isinstance(e, requests.exceptions.ConnectionError):
        return FRIENDLY_ERROR
    if "HTTP 429" in str(e):
        return "Price service rate limit reached. Please try again shortly."
    if "HTTP" in str(e):
        return FRIENDLY_ERROR

    return FRIENDLY_ERROR


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
        return error(_friendly_error(e, symbol))


def get_prices(symbols):
    if not FINNHUB_API_KEY:
        return error("Finnhub API key not configured.")

    result = []

    try:
        for symbol in symbols:
            symbol = symbol.upper()
            data = _quote(symbol)

            price = data.get("c")

            if not price:
                result.append({
                    "symbol": symbol,
                    "price": None,
                    "high": None,
                    "low": None,
                    "open": None,
                    "previous_close": None,
                })
                continue

            result.append({
                "symbol": symbol,
                "price": price,
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
        return error(_friendly_error(e))
