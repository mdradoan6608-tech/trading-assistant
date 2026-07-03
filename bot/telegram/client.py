from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

import datetime as dt

from telegram.ext import ContextTypes as _ContextTypes

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from bot.telegram.handler import handle_message
from storage.watchlist import get_watchlist
from core.signal import signal
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
            "/analyze SYMBOL\n"
            "/price SYMBOL\n"
            "/watchlist\n"
            "/watchlist add SYMBOL\n"
            "/watchlist remove SYMBOL\n"
            "/market"
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/status")
        data = response["data"]

        await update.message.reply_text(
            f"🤖 {data['app']}\n\n"
            f"Status : Running ✅\n"
            f"Version : {data['version']}"
        )

    async def whoami(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/whoami", user=self.get_user(update))
        data = response["data"]

        await update.message.reply_text(
            "👤 User Information\n\n"
            f"Name : {data['name']}\n"
            f"Username : @{data['username']}\n"
            f"User ID : {data['id']}"
        )

    async def portfolio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/portfolio", user=self.get_user(update))

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        await update.message.reply_text(
            "📈 Portfolio\n\n"
            f"Broker : {data['broker']}\n"
            f"Connected : {data['connected']}"
        )

    async def connection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/connection", user=self.get_user(update))

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]
        status = "Connected ✅" if data["connected"] else "Disconnected ❌"

        await update.message.reply_text(
            "🔌 IBKR Connection\n\n"
            f"Broker : {data['broker']}\n"
            f"Status : {status}"
        )

    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage:\n/analyze SYMBOL")
            return

        response = handle_message(f"/analyze {context.args[0].upper()}")

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        await update.message.reply_text(
            f"📊 Analysis for {data['symbol']}\n\n"
            f"Status:\n{data['status']}\n\n"
            f"Recommendation:\n{data['recommendation']}"
        )

    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage:\n/price SYMBOL")
            return

        response = handle_message(f"/price {context.args[0].upper()}")

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        await update.message.reply_text(
            f"💲 {data['symbol']}\n\n"
            f"Current : {data['price']}\n"
            f"Open : {data['open']}\n"
            f"High : {data['high']}\n"
            f"Low : {data['low']}\n"
            f"Previous Close : {data['previous_close']}"
        )

    async def market(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = handle_message("/market")

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        prices = response["data"]["prices"]
        is_open = response["data"].get("is_open", False)

        text = "🌍 US Market\n\n"
        text += "```\n"

        names = {
            "SPY": "S&P 500",
            "QQQ": "Nasdaq",
            "DIA": "Dow Jones",
        }

        for item in prices:
            price = item["price"]
            previous = item["previous_close"]

            change = (price - previous) / previous * 100

            dot = "🟢" if change >= 0 else "🔴"
            sign = "+" if change >= 0 else ""

            text += (
                f"{dot} "
                f"{names.get(item['symbol'], item['symbol']):<10} "
                f"{sign}{change:.2f}%\n"
            )

        text += "```\n\n"

        status_dot = "🟢" if is_open else "🔴"
        status_label = "OPEN" if is_open else "CLOSED"

        text += f"Market Status:\n{status_dot} {status_label}"

        await update.message.reply_text(
            text,
            parse_mode="Markdown",
        )

    async def signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage:\n/signal SYMBOL")
            return

        response = handle_message(f"/signal {context.args[0].upper()}")

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        data = response["data"]

        text = f"📐 {data['symbol']}\n\n"
        text += f"Stage : {data['stage_label']}\n\n"

        for label, passed in data["checks"]:
            mark = "✔" if passed else "✖"
            text += f"{mark} {label}\n"

        if not data["checks"]:
            text += "No price action setup detected.\n"

        text += "\n"
        text += "```\n"
        text += f"Close        : {data['close']}\n"
        text += f"RSI(14)      : {data['rsi']}\n"
        text += f"RSI EMA9     : {data['rsi_ema9']}\n"
        text += f"MACD         : {data['macd']}\n"
        text += f"MACD Signal  : {data['macd_signal']}\n"
        text += f"MACD Hist    : {data['macd_histogram']}\n"
        text += "```"

        await update.message.reply_text(text, parse_mode="Markdown")

    def _format_watchlist_line(self, item):
        symbol = item.get("symbol", "?")
        price = item.get("price")
        previous_close = item.get("previous_close")

        if price is None:
            return f"⚪ {symbol}"

        if previous_close:
            change_pct = (price - previous_close) / previous_close * 100
            dot = "🟢" if change_pct >= 0 else "🔴"
            sign = "+" if change_pct >= 0 else ""
            change_str = f"{sign}{change_pct:.2f}%"
        else:
            dot = "⚪"
            change_str = "N/A"

        return f"{dot} {symbol:<6} ${price:<9.2f} {change_str}"

    async def watchlist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        args = context.args if context.args else ["list"]
        command = "/watchlist " + " ".join(args)

        response = handle_message(command)

        if not response["success"]:
            await update.message.reply_text(response["message"])
            return

        prices = response["data"].get("prices")

        if prices is None:
            symbols = response["data"].get("watchlist", [])
            if not symbols:
                await update.message.reply_text("📋 Watchlist is empty.")
                return
            text = "📋 Watchlist\n\n"
            for symbol in symbols:
                text += f"• {symbol}\n"
            await update.message.reply_text(text)
            return

        if not prices:
            await update.message.reply_text("📋 Watchlist is empty.")
            return

        text = "📋 Watchlist\n\n"
        text += "```\n"

        for item in prices:
            text += self._format_watchlist_line(item) + "\n"

        text += "```\n\n"

        now_uae = datetime.now(ZoneInfo("Asia/Dubai"))
        time_str = now_uae.strftime("%I:%M %p UAE").lstrip("0")

        text += f"Last Updated:\n{time_str}"

        await update.message.reply_text(text, parse_mode="Markdown")

    async def daily_signal_scan(self, context: _ContextTypes.DEFAULT_TYPE):
        symbols = get_watchlist()

        if not symbols:
            return

        alerts = []

        for symbol in symbols:
            result = signal(symbol)

            if not result["success"]:
                continue

            data = result["data"]

            if data["stage"] >= 3:
                alerts.append(data)

        if not alerts:
            return

        text = "📡 Daily Signal Scan\n\n"

        for data in alerts:
            text += f"{data['symbol']} — {data['stage_label']}\n"

        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
        )

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
        app.add_handler(CommandHandler("price", self.price))
        app.add_handler(CommandHandler("watchlist", self.watchlist))
        app.add_handler(CommandHandler("market", self.market))
        app.add_handler(CommandHandler("signal", self.signal))

        app.job_queue.run_daily(
            self.daily_signal_scan,
            time=dt.time(hour=15, minute=30, tzinfo=ZoneInfo("Asia/Dubai")),
        )

        logger.info("Telegram bot is starting...")

        app.run_polling()
