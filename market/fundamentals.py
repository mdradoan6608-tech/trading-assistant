import yfinance as yf

from core.response import success, error


def get_fundamentals(symbol):
    symbol = symbol.upper()

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        market_cap = info.get("marketCap")
        pe_ratio = info.get("trailingPE")
        eps = info.get("trailingEps")
        dividend_yield = info.get("dividendYield")
        week_52_high = info.get("fiftyTwoWeekHigh")
        week_52_low = info.get("fiftyTwoWeekLow")

        return success(
            f"Fundamentals for {symbol}",
            {
                "symbol": symbol,
                "market_cap": market_cap,
                "pe_ratio": round(pe_ratio, 2) if pe_ratio else None,
                "eps": round(eps, 2) if eps else None,
                "dividend_yield": round(dividend_yield, 2) if dividend_yield else None,
                "week_52_high": week_52_high,
                "week_52_low": week_52_low,
            },
        )

    except Exception as e:
        return error(str(e))
