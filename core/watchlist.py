from core.response import success, error
from storage.watchlist import (
    get_watchlist,
    save_watchlist,
)
from market.provider import get_prices


def _parse_symbols(raw_input):
    parts = raw_input.split(",")
    return [p.strip().upper() for p in parts if p.strip()]


def add(symbol):
    requested = _parse_symbols(symbol)

    symbols = get_watchlist()

    added = []
    skipped = []

    for sym in requested:
        if sym in symbols:
            skipped.append(sym)
            continue
        symbols.append(sym)
        added.append(sym)

    save_watchlist(symbols)

    if not added:
        return error(f"Already in watchlist: {', '.join(skipped)}")

    message = f"Added: {', '.join(added)}"
    if skipped:
        message += f"\nAlready exists: {', '.join(skipped)}"

    return success(
        message,
        {"watchlist": symbols},
    )


def remove(symbol):
    requested = _parse_symbols(symbol)

    symbols = get_watchlist()

    removed = []
    not_found = []

    for sym in requested:
        if sym not in symbols:
            not_found.append(sym)
            continue
        symbols.remove(sym)
        removed.append(sym)

    save_watchlist(symbols)

    if not removed:
        return error(f"Not found: {', '.join(not_found)}")

    message = f"Removed: {', '.join(removed)}"
    if not_found:
        message += f"\nNot found: {', '.join(not_found)}"

    return success(
        message,
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
