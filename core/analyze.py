import json
import time

from core.response import success, error
from market.provider import get_prices
from market.fundamentals import get_fundamentals
from market.news import get_news
from strategies.indicators import get_indicators
from strategies.stage_engine import evaluate_stage
from ai.engine import ask_ai


def _format_market_cap(value):
    if not value:
        return "N/A"
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value}"


def _news_sentiment(symbol, news_items):
    if not news_items:
        return {"summary": "No recent news", "counts": None}

    headlines = "\n".join(
        f"- {item.get('headline', '')}" for item in news_items[:5]
    )

    prompt = f"""Here are recent headlines for {symbol}:

{headlines}

Classify overall sentiment. Respond ONLY in this exact JSON format, no other text:
{{"overall": "Positive/Negative/Mixed/Neutral", "positive": <count>, "negative": <count>, "neutral": <count>}}
"""

    result = ask_ai(prompt)

    if not result["success"]:
        return {"summary": "Unavailable", "counts": None}

    try:
        cleaned = result["data"]["text"].strip().strip("```").replace("json", "", 1).strip()
        parsed = json.loads(cleaned)
        return {
            "summary": parsed.get("overall", "Neutral"),
            "counts": (parsed.get("positive", 0), parsed.get("neutral", 0), parsed.get("negative", 0)),
        }
    except Exception:
        return {"summary": "Unavailable", "counts": None}


def _ai_summary(symbol, price_data, stage_info, news_summary, trend, risk):
    prompt = f"""Write a 2-3 sentence plain-language trading summary for {symbol} based on:

Price: {price_data['price']} ({price_data['change_pct']:+.2f}%)
Technical signal: {stage_info['label']}
News sentiment: {news_summary}
Trend: {trend}
Risk: {risk}

Be neutral and factual. Do not give specific buy/sell price targets or guarantees. End with a note that final decision is up to the user.
"""

    result = ask_ai(prompt)

    if not result["success"]:
        return "AI summary unavailable right now."

    return result["data"]["text"].strip()


def analyze_symbol(symbol):
    symbol = symbol.upper()

    price_result = get_prices([symbol])
    if not price_result["success"]:
        return price_result

    price_item = price_result["data"]["prices"][0]
    price = price_item.get("price")
    previous_close = price_item.get("previous_close")

    if price is None or previous_close is None:
        return error(f"No price data available for {symbol}.")

    change_pct = (price - previous_close) / previous_close * 100

    indicator_result = get_indicators(symbol)
    if not indicator_result["success"]:
        return indicator_result

    indicator_data = indicator_result["data"]
    stage_info = evaluate_stage(indicator_data)

    fundamentals_result = get_fundamentals(symbol)
    fundamentals = fundamentals_result["data"] if fundamentals_result["success"] else {}

    week_52_high = fundamentals.get("week_52_high")
    week_52_low = fundamentals.get("week_52_low")

    position_pct = None
    if week_52_high and week_52_low and week_52_high != week_52_low:
        position_pct = (price - week_52_low) / (week_52_high - week_52_low) * 100

    news_result = get_news(symbol, days_back=3)
    news_items = news_result["data"]["news"] if news_result["success"] else []
    sentiment = _news_sentiment(symbol, news_items)

    time.sleep(5)

    trend = "Bullish" if stage_info["direction"] == "BUY" else (
        "Bearish" if stage_info["direction"] == "SELL" else "Neutral"
    )

    if position_pct is not None and position_pct >= 90:
        risk = "Medium (near 52-week high, pullback possible)"
    elif position_pct is not None and position_pct <= 10:
        risk = "Medium (near 52-week low, volatility possible)"
    else:
        risk = "Low to Medium"

    ai_summary = _ai_summary(
        symbol,
        {"price": price, "change_pct": change_pct},
        stage_info,
        sentiment["summary"],
        trend,
        risk,
    )

    return success(
        f"Analysis for {symbol}",
        {
            "symbol": symbol,
            "price": round(price, 2),
            "change_pct": round(change_pct, 2),
            "stage_label": stage_info["label"],
            "position_pct": round(position_pct, 1) if position_pct is not None else None,
            "market_cap": _format_market_cap(fundamentals.get("market_cap")),
            "pe_ratio": fundamentals.get("pe_ratio") or "N/A",
            "eps": fundamentals.get("eps") or "N/A",
            "dividend_yield": fundamentals.get("dividend_yield"),
            "news_summary": sentiment["summary"],
            "news_counts": sentiment["counts"],
            "trend": trend,
            "risk": risk,
            "ai_summary": ai_summary,
        },
    )
