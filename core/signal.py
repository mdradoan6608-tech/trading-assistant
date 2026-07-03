from strategies.indicators import get_indicators


def signal(symbol):
    return get_indicators(symbol)
