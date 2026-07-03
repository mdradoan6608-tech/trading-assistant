from core.response import success
from core.market import market
from storage.watchlist import get_watchlist
from storage.signal_history import get_last_stages, save_last_stages
from core.signal import signal


def build_overview():
    market_result = market()
    market_prices = market_result["data"]["prices"] if market_result["success"] else []

    symbols = get_watchlist()
    last_stages = get_last_stages()

    watchlist_items = []
    new_stages = {}

    for sym in symbols:
        result = signal(sym)

        if not result["success"]:
            continue

        data = result["data"]

        previous_stage = last_stages.get(sym)
        current_stage = data["stage"]
        direction = data["direction"]

        changed = previous_stage is not None and previous_stage != current_stage

        watchlist_items.append({
            "symbol": sym,
            "close": data["close"],
            "stage": current_stage,
            "stage_label": data["stage_label"],
            "direction": direction,
            "changed": changed,
        })

        new_stages[sym] = current_stage

    save_last_stages(new_stages)

    return success(
        "Overview",
        {
            "market": market_prices,
            "watchlist": watchlist_items,
        },
    )
