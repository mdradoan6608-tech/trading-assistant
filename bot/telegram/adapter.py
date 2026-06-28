from core.command_router import execute


def process_message(message: str):
    """
    Convert Telegram message to a core command.
    """

    command = message.strip().lstrip("/")

    return execute(command)
