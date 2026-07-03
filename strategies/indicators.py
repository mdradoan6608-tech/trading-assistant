import yfinance as yf
import pandas as pd

from core.response import success, error


def get_indicators(symbol, period="6mo"):
    symbol = symbol.upper()

    try:
        df = yf.download(
            symbol,
            period=period,
            interval="1d",
            progress=False,
            auto_adjust=True,
        )

        if df.empty:
            return error(f"No historical data found for {symbol}.")

        close = df["Close"].squeeze()

        # RSI (14) with EMA smoothing (Wilder-style via EWM)
        delta = close.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_ema9 = rsi.ewm(span=9, adjust=False).mean()

        # MACD (12, 26, 9)
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line

        return success(
            f"Indicators for {symbol}",
            {
                "symbol": symbol,
                "close": round(float(close.iloc[-1]), 2),
                "rsi": round(float(rsi.iloc[-1]), 2),
                "rsi_ema9": round(float(rsi_ema9.iloc[-1]), 2),
                "macd": round(float(macd_line.iloc[-1]), 2),
                "macd_signal": round(float(signal_line.iloc[-1]), 2),
                "macd_histogram": round(float(histogram.iloc[-1]), 2),
                "histogram_series": [round(float(x), 2) for x in histogram.tail(5)],
            },
        )

    except Exception as e:
        return error(str(e))
