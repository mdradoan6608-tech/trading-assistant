from bot.telegram.adapter import process_message


def handle_message(text, user=None):
    return process_message(text, user=user)
