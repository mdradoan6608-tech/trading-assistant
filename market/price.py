import yfinance as yf

from core.response import success, error


def get_price(symbol):
    symbol = symbol.upper()

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info

        price = info.get("lastPrice")

        if price is None:
            return error("Price not available.")

        return success(
            f"Price for {symbol}",
            {
                "symbol": symbol,
                "price": round(price, 2),
            },
        )

    except Exception as e:
        return error(str(e))
