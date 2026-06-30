from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config.settings import TELEGRAM_BOT_TOKEN
from bot.telegram.handler import handle_message
from utils.logger import logger


class TelegramService:

    def get_user(self, update: Update):
        return {
            "id": update.effective_user.id,
            "name": update.effective_user.full_name,
            "username": update.effective_user.username or "",
        }

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🏓 Pong!")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "/help\n"
            "/ping\n"
            "/status\n"
            "/whoami\n"
            "/portfolio\n"
            "/connection\n"
            "/analyze SYMBOL"
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/status")

        data = response["data"]

        text = (
            f"🤖 {data['app']}\n\n"
            f"Status : Running ✅\n"
            f"Version : {data['version']}"
        )

        await update.message.reply_text(text)

    async def whoami(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/whoami", user=self.get_user(update))

        data = response["data"]

        text = (
            "👤 User Information\n\n"
            f"Name : {data['name']}\n"
            f"Username : @{data['username']}\n"
            f"User ID : {data['id']}"
        )

        await update.message.reply_text(text)

    async def portfolio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/portfolio", user=self.get_user(update))

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        text = (
            "📈 Portfolio\n\n"
            f"Broker : {data['broker']}\n"
            f"Connected : {data['connected']}"
        )

        await update.message.reply_text(text)

    async def connection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/connection", user=self.get_user(update))

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        status = "Connected ✅" if data["connected"] else "Disconnected ❌"

        text = (
            "🔌 IBKR Connection\n\n"
            f"Broker : {data['broker']}\n"
            f"Status : {status}"
        )

        await update.message.reply_text(text)

    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text(
                "Usage:\n/analyze SYMBOL\n\nExample:\n/analyze AAPL"
            )
            return

        symbol = context.args[0].upper()

        response = handle_message(f"/analyze {symbol}")

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        text = (
            f"📊 Analysis for {data['symbol']}\n\n"
            f"Status:\n{data['status']}\n\n"
            f"Recommendation:\n{data['recommendation']}"
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
        app.add_handler(CommandHandler("portfolio", self.portfolio))
        app.add_handler(CommandHandler("connection", self.connection))
        app.add_handler(CommandHandler("analyze", self.analyze))

        logger.info("Telegram bot is starting...")

        app.run_polling()
