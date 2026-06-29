from core.authorization import authorize
from core.commands import COMMANDS
from core.response import error


def execute(command, user=None):
    command = command.lower()

    if command not in COMMANDS:
        return error("Unknown command")

    auth_result = authorize(command, user)

    if auth_result is not None:
        return auth_result

    if command == "whoami":
        return COMMANDS[command](user)

    return COMMANDS[command]()
