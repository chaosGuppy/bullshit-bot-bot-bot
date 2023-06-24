import os
import logging
from bullshit_bot_bot_bot.handlers.summarize import summarize
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from middleware import telegram_updates_to_generic_thread

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=str(telegram_updates_to_generic_thread(context.chat_data["updates"])),
    )


async def record_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "updates" not in context.chat_data:
        context.chat_data["updates"] = []
    context.chat_data["updates"].append(update.to_dict())


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()

    start_handler = CommandHandler("start", start)
    summarize_handler = CommandHandler("summarize", summarize)

    application.add_handler(summarize_handler)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.ALL, record_messages))

    application.run_polling()
