from core.response import success, error
from storage.watchlist import (
    get_watchlist,
    save_watchlist,
)
from market.provider import get_prices


def add(symbol):
    symbol = symbol.upper()

    symbols = get_watchlist()

    if symbol in symbols:
        return error(f"{symbol} already exists.")

    symbols.append(symbol)

    save_watchlist(symbols)

    return success(
        f"{symbol} added.",
        {"watchlist": symbols},
    )


def remove(symbol):
    symbol = symbol.upper()

    symbols = get_watchlist()

    if symbol not in symbols:
        return error(f"{symbol} not found.")

    symbols.remove(symbol)

    save_watchlist(symbols)

    return success(
        f"{symbol} removed.",
        {"watchlist": symbols},
    )


def show():
    symbols = get_watchlist()

    if not symbols:
        return success(
            "Watchlist",
            {
                "watchlist": [],
                "prices": [],
            },
        )

    prices = get_prices(symbols)

    if not prices["success"]:
        return prices

    return success(
        "Watchlist",
        {
            "watchlist": symbols,
            "prices": prices["data"]["prices"],
        },
    )
