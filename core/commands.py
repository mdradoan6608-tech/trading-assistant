from core.health import status, health
from core.user import whoami

COMMANDS = {
    "status": status,
    "health": health,
    "whoami": whoami,
}
