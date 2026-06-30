from core.command_router import execute
from core.commands import (
    execute_analysis,
    execute_price,
)


def process_message(text, user=None):
    text = text.strip()

    if text.startswith("/"):
        text = text[1:]

    parts = text.split(maxsplit=1)

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

    return execute(command, user=user)
