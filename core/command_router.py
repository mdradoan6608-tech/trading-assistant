from core.commands import COMMANDS
from core.response import error


def execute(command, **kwargs):
    command = command.lower()

    if command in COMMANDS:
        return COMMANDS[command](**kwargs)

    return error("Unknown command")
