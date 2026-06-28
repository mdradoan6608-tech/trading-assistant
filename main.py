from bot.telegram.client import TelegramService
from services.manager import ServiceManager


def main():
    manager = ServiceManager()

    manager.register("telegram", TelegramService())

    manager.start()


if __name__ == "__main__":
    main()
