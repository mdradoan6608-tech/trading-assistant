from core.health import status, health
from core.user import whoami
from core.portfolio import portfolio
from core.connection import connection

COMMANDS = {
    "status": status,
    "health": health,
    "whoami": whoami,
    "portfolio": portfolio,
    "connection": connection,
}
