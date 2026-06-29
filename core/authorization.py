from core.auth import is_authorized
from core.response import error


PUBLIC_COMMANDS = {
    "ping",
    "help",
    "status",
    "health",
    "whoami",
}


def authorize(command, user=None):
    command = command.lower()

    if command in PUBLIC_COMMANDS:
        return None

    if user is None:
        return error("Authorization required.")

    if not is_authorized(user["id"]):
        return error("Unauthorized user.")

    return None
