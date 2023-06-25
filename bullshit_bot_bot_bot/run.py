import os
import logging
from bullshit_bot_bot_bot.handlers.conflicts import get_conflicts
from bullshit_bot_bot_bot.handlers.factcheck import factcheck
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
from bullshit_bot_bot_bot.handlers.missing_considerations import (
    get_missing_considerations,
)
from bullshit_bot_bot_bot.handlers.sources import extract_claims, get_sources

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=str(
            telegram_updates_to_generic_thread(context.chat_data.get("updates", []))
        ),
    )


async def missing_considerations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_text = get_missing_considerations(
        telegram_updates_to_generic_thread(context.chat_data.get("updates", []))
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text,
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)


async def record_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "updates" not in context.chat_data:
        context.chat_data["updates"] = []
    context.chat_data["updates"].append(update.to_dict())


async def claims(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = telegram_updates_to_generic_thread(context.chat_data.get("updates", []))
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=extract_claims(messages)
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()

    start_handler = CommandHandler("start", start)
    summarize_handler = CommandHandler("summarize", summarize)
    missing_considerations_handler = CommandHandler(
        "missing_considerations", missing_considerations
    )
    sources_handler = CommandHandler("sources", get_sources)
    claims_handler = CommandHandler("claims", claims)
    factcheck_handler = CommandHandler("factcheck", factcheck)
    conflicts_handler = CommandHandler("conflicts", get_conflicts)

    application.add_handler(start_handler)
    application.add_handler(summarize_handler)
    application.add_handler(missing_considerations_handler)
    application.add_handler(sources_handler)
    application.add_handler(claims_handler)
    application.add_handler(factcheck_handler)
    application.add_handler(conflicts_handler)
    application.add_handler(MessageHandler(filters.ALL, record_messages))
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
