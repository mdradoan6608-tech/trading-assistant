from brokers.ibkr.account import connection_status
from core.response import success


def connection():
    data = connection_status()

    return success(
        "IBKR connection status",
        data,
    )
