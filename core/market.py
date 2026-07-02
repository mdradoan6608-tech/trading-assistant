from core.response import success, error
from market.provider import get_prices


def market():
    symbols = ["SPY", "QQQ", "DIA"]

    result = get_prices(symbols)

    if not result["success"]:
        return result

    return success(
        "Market",
        {
            "prices": result["data"]["prices"],
        },
    )
