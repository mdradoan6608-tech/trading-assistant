from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config.settings import TELEGRAM_BOT_TOKEN
from bot.telegram.handler import handle_message
from utils.logger import logger


class TelegramService:

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/status")

        text = (
            f"🤖 {response['data']['app']}\n\n"
            f"Status : Running ✅\n"
            f"Version : {response['data']['version']}"
        )

        await update.message.reply_text(text)

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🏓 Pong!")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "/help\n"
            "/ping\n"
            "/status\n"
            "/whoami"
        )

    async def whoami(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = {
            "id": update.effective_user.id,
            "name": update.effective_user.full_name,
            "username": update.effective_user.username or "",
        }

        response = handle_message("/whoami", user=user)

        data = response["data"]

        text = (
            "👤 User Information\n\n"
            f"Name : {data['name']}\n"
            f"Username : @{data['username']}\n"
            f"User ID : {data['id']}"
        )

        await update.message.reply_text(text)

    def start(self):
        if not TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram token not configured.")
            return

        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("help", self.help))
        app.add_handler(CommandHandler("ping", self.ping))
        app.add_handler(CommandHandler("status", self.status))
        app.add_handler(CommandHandler("whoami", self.whoami))

        logger.info("Telegram bot is starting...")

        app.run_polling()
