from core.health import status, health
from core.user import whoami
from core.portfolio import portfolio
from core.connection import connection
from core.analyze import analyze_symbol
from core.price import price

COMMANDS = {
    "status": status,
    "health": health,
    "whoami": whoami,
    "portfolio": portfolio,
    "connection": connection,
}


def execute_analysis(symbol):
    return analyze_symbol(symbol)


def execute_price(symbol):
    return price(symbol)
