import requests

from config.settings import FINNHUB_API_KEY
from core.response import success, error
from utils.logger import logger

BASE_URL = "https://finnhub.io/api/v1/company-news"

FRIENDLY_ERROR = "News service is temporarily unavailable. Please try again in a few minutes."


def get_news(symbol, days_back=1):
    symbol = symbol.upper()

    if not FINNHUB_API_KEY:
        return error("Finnhub API key not configured.")

    try:
        import datetime

        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=days_back)

        url = (
            f"{BASE_URL}?symbol={symbol}"
            f"&from={from_date.isoformat()}"
            f"&to={today.isoformat()}"
            f"&token={FINNHUB_API_KEY}"
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return error(f"HTTP {response.status_code}")

        articles = response.json()

        news_items = [
            {
                "headline": item.get("headline"),
                "summary": item.get("summary"),
                "url": item.get("url"),
                "datetime": item.get("datetime"),
                "id": item.get("id"),
            }
            for item in articles[:5]
        ]

        return success(
            f"News for {symbol}",
            {"symbol": symbol, "news": news_items},
        )

    except Exception as e:
        logger.error(f"Finnhub news error for {symbol}: {e}")
        return error(FRIENDLY_ERROR)
