from core.response import success


def portfolio():
    return success(
        "Portfolio module is ready.",
        {
            "broker": "IBKR",
            "connected": False,
        },
    )
