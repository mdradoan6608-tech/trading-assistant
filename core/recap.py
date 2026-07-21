from collections import defaultdict

from core.response import success
from storage.signal_log import get_entries_since


def build_recap(days_back=7):
    entries = get_entries_since(days_back)

    if not entries:
        return success(
            "Weekly Recap",
            {"has_data": False, "symbols": []},
        )

    by_symbol = defaultdict(list)
    for entry in entries:
        by_symbol[entry["symbol"]].append(entry)

    summary = []
    for symbol, symbol_entries in by_symbol.items():
        symbol_entries.sort(key=lambda e: e["timestamp"])

        buy_count = sum(1 for e in symbol_entries if e["direction"] == "BUY")
        sell_count = sum(1 for e in symbol_entries if e["direction"] == "SELL")

        first = symbol_entries[0]
        last = symbol_entries[-1]

        summary.append({
            "symbol": symbol,
            "buy_count": buy_count,
            "sell_count": sell_count,
            "first_date": first["date"],
            "first_direction": first["direction"],
            "first_price": first["price"],
            "last_date": last["date"],
            "last_direction": last["direction"],
            "last_price": last["price"],
        })

    summary.sort(key=lambda s: s["symbol"])

    return success(
        "Weekly Recap",
        {"has_data": True, "symbols": summary, "days_back": days_back},
    )
