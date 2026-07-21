from datetime import datetime
from zoneinfo import ZoneInfo

from storage.json_store import load, save

FILE = "storage/signal_log.json"


def log_signal(symbol, direction, price):
    data = load(FILE, {"entries": []})

    now = datetime.now(ZoneInfo("Asia/Dubai"))
    today_str = now.strftime("%Y-%m-%d")

    for entry in data["entries"]:
        if entry["symbol"] == symbol and entry["date"] == today_str and entry["direction"] == direction:
            return

    data["entries"].append({
        "symbol": symbol,
        "direction": direction,
        "price": price,
        "date": today_str,
        "timestamp": now.isoformat(),
    })

    data["entries"] = data["entries"][-500:]

    save(FILE, data)


def get_entries_since(days_back=7):
    data = load(FILE, {"entries": []})

    now = datetime.now(ZoneInfo("Asia/Dubai"))
    cutoff = now.timestamp() - (days_back * 86400)

    result = []
    for entry in data["entries"]:
        try:
            entry_time = datetime.fromisoformat(entry["timestamp"]).timestamp()
            if entry_time >= cutoff:
                result.append(entry)
        except Exception:
            continue

    return result
