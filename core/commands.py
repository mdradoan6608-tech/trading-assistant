from core.health import status, health
from core.user import whoami
from core.portfolio import portfolio
from core.connection import connection
from core.analyze import analyze_symbol

COMMANDS = {
    "status": status,
    "health": health,
    "whoami": whoami,
    "portfolio": portfolio,
    "connection": connection,
}


def execute_analysis(symbol):
    return analyze_symbol(symbol)
