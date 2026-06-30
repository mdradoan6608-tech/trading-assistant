from core.command_router import execute
from core.commands import (
    execute_analysis,
    execute_price,
    execute_watchlist,
)


def process_message(text, user=None):
    text = text.strip()

    if text.startswith("/"):
        text = text[1:]

    parts = text.split(maxsplit=2)

    command = parts[0].lower()

    if command == "analyze":
        if len(parts) < 2:
            return {
                "success": False,
                "message": "Usage: /analyze SYMBOL",
                "data": {},
            }

        return execute_analysis(parts[1])

    if command == "price":
        if len(parts) < 2:
            return {
                "success": False,
                "message": "Usage: /price SYMBOL",
                "data": {},
            }

        return execute_price(parts[1])

    if command == "watchlist":
        if len(parts) < 2:
            return {
                "success": False,
                "message": "Usage: /watchlist list | add SYMBOL | remove SYMBOL",
                "data": {},
            }

        action = parts[1].lower()
        symbol = parts[2] if len(parts) > 2 else None

        return execute_watchlist(action, symbol)

    return execute(command, user=user)
