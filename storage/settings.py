from storage.json_store import load, save

FILE = "storage/settings.json"


def get_news_alert_enabled():
    data = load(FILE, {"news_alert_enabled": True})
    return data.get("news_alert_enabled", True)


def set_news_alert_enabled(enabled):
    data = load(FILE, {"news_alert_enabled": True})
    data["news_alert_enabled"] = enabled
    save(FILE, data)
