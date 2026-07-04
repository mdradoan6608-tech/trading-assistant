from storage.json_store import load, save

FILE = "storage/news_history.json"


def get_seen_ids():
    data = load(FILE, {"seen": []})
    return set(data["seen"])


def save_seen_ids(seen_ids):
    save(FILE, {"seen": list(seen_ids)})
