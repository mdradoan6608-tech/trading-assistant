from storage.json_store import load, save

FILE = "storage/signal_history.json"


def get_last_stages():
    data = load(FILE, {"stages": {}})
    return data["stages"]


def save_last_stages(stages):
    save(FILE, {"stages": stages})
