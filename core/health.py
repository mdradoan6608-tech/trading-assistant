from core.response import success
from core.version import APP_NAME, VERSION


def status():
    return success(
        "Trading Assistant is running",
        {
            "app": APP_NAME,
            "version": VERSION,
        },
    )


def health():
    return success(
        "Trading Assistant is healthy",
        {
            "status": "ok",
            "version": VERSION,
        },
    )
