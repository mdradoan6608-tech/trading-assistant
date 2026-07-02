from datetime import datetime
from zoneinfo import ZoneInfo

from core.response import success, error
from market.provider import get_prices


def _is_market_open():
    now_et = datetime.now(ZoneInfo("America/New_York"))

    if now_et.weekday() >= 5:
        return False

    open_time = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
    close_time = now_et.replace(hour=16, minute=0, second=0, microsecond=0)

    return open_time <= now_et <= close_time


def market():
    symbols = ["SPY", "QQQ", "DIA"]

    result = get_prices(symbols)

    if not result["success"]:
        return result

    return success(
        "Market",
        {
            "prices": result["data"]["prices"],
            "is_open": _is_market_open(),
        },
    )
