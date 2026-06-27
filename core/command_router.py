from core.commands import COMMANDS


def execute(command):
    command = command.lower()

    if command in COMMANDS:
        return COMMANDS[command]()

    return {
        "error": "Unknown command"
    }
