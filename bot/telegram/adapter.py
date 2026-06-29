from core.command_router import execute


def process_message(text, user=None):
    text = text.strip()

    if text.startswith("/"):
        text = text[1:]

    if text == "whoami":
        return execute(text, user=user)

    return execute(text)
