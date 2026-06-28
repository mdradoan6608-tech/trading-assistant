from core.response import success


def status():
    return success(
        "Trading Assistant is running",
        {
            "app": "Trading Assistant",
            "version": "0.1.0"
        }
    )
