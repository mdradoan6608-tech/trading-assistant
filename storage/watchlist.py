from storage.json_store import load, save

FILE = "storage/watchlist.json"


def get_watchlist():
    data = load(FILE, {"symbols": []})
    return data["symbols"]


def save_watchlist(symbols):
    save(FILE, {"symbols": symbols})
