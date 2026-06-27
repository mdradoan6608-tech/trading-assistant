import time

from config.settings import TELEGRAM_BOT_TOKEN
from utils.logger import logger

APP_NAME = "Trading Assistant"


def main():
    logger.info("=" * 40)
    logger.info(f"{APP_NAME} is starting...")
    logger.info("Running on Railway Cloud")

    if TELEGRAM_BOT_TOKEN:
        logger.info("Telegram bot token loaded.")
    else:
        logger.warning("Telegram bot token is not configured.")

    logger.info("=" * 40)

    while True:
        logger.info("Trading Assistant is alive...")
        time.sleep(60)


if __name__ == "__main__":
    main()
