from core.command_router import execute


def process_message(text, user=None):
    text = text.strip()

    if text.startswith("/"):
        text = text[1:]

    return execute(text, user=user)
