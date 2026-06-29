from brokers.ibkr.client import IBKRClient

client = IBKRClient()


def connection_status():
    return {
        "broker": "IBKR",
        "connected": client.is_connected(),
    }
