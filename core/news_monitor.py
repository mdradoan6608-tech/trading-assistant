import json
import asyncio

from core.response import success
from storage.watchlist import get_watchlist
from storage.news_history import get_seen_ids, save_seen_ids
from market.news import get_news
from ai.engine import ask_ai


FILTER_PROMPT = """A stock news headline and summary is given below for {symbol}.

Headline: {headline}
Summary: {summary}

Decide if this news is likely to meaningfully move the stock price (earnings, major product news, legal/regulatory action, executive changes, M&A, major guidance changes, etc). Ignore routine/minor news (small partnerships, minor analyst notes, generic market commentary).

Respond ONLY in this exact JSON format, no other text:
{{"important": true or false, "analysis": "1-2 sentence plain-language explanation of impact and direction (bullish/bearish/neutral), in simple words"}}
"""


async def check_watchlist_news():
    symbols = get_watchlist()
    seen_ids = get_seen_ids()

    alerts = []

    for symbol in symbols:
        result = get_news(symbol, days_back=1)

        if not result["success"]:
            continue

        articles = result["data"]["news"]

        for article in articles:
            article_id = article.get("id")

            if article_id is None or article_id in seen_ids:
                continue

            seen_ids.add(article_id)

            headline = article.get("headline", "")
            summary = article.get("summary", "")

            if not headline:
                continue

            prompt = FILTER_PROMPT.format(
                symbol=symbol,
                headline=headline,
                summary=summary,
            )

            await asyncio.sleep(5)
            ai_result = ask_ai(prompt)

            if not ai_result["success"]:
                continue

            raw_text = ai_result["data"]["text"]

            try:
                cleaned = raw_text.strip().strip("```").replace("json", "", 1).strip()
                parsed = json.loads(cleaned)
            except Exception:
                continue

            if parsed.get("important"):
                alerts.append({
                    "symbol": symbol,
                    "headline": headline,
                    "analysis": parsed.get("analysis", ""),
                })

    save_seen_ids(seen_ids)

    return success("News check complete", {"alerts": alerts})
