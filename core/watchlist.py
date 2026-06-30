from core.response import success, error
from storage.watchlist import (
    get_watchlist,
    save_watchlist,
)


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
    return success(
        "Watchlist",
        {
            "watchlist": get_watchlist(),
        },
    )
