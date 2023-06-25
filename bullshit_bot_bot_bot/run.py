import os
from typing import Callable
import logging
from bullshit_bot_bot_bot.handlers.conflicts import get_conflicts
from bullshit_bot_bot_bot.handlers.factcheck import factcheck
from bullshit_bot_bot_bot.handlers.summarize import summarize
from bullshit_bot_bot_bot.handlers.sources import evidence
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from middleware import telegram_updates_to_generic_thread
from bullshit_bot_bot_bot.handlers.missing_considerations import (
    missing_considerations,
)

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


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)


async def record_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "updates" not in context.chat_data:
        context.chat_data["updates"] = []
    context.chat_data["updates"].append(update.to_dict())


class CommandRegistry:
    def __init__(self, application: Application):
        self._application = application
        self._command_descriptions = {}

    def register(self, command_name: str, callback: Callable, description: str):
        self._application.add_handler(CommandHandler(command_name, callback))
        self._command_descriptions[command_name] = description

    def get_onboarding_message(self):
        return "Here's what I can do:\n" + "\n".join(
            f"/{command_name}: {description}"
            for command_name, description in self._command_descriptions.items()
        )


class OnboardingCommand:
    def __init__(self, registry: CommandRegistry):
        self._registry = registry

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self._registry.get_onboarding_message(),
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    registry = CommandRegistry(application)

    registry.register(
        "f",
        factcheck,
        "Factcheck claims from the last message using the Google fact check API. "
        "Use '/f all' to process the whole conversation.",
    )
    registry.register(
        "e",
        evidence,
        "Find evidence that supports or refutes the claims in the last message. "
        "Use '/e all' to process the whole conversation.",
    )
    registry.register(
        "c",
        get_conflicts,
        "Get a list of actors who may have an interest in having people believe "
        "the claims in the last message. Use '/c all' to process the whole "
        "conversation.",
    )
    registry.register(
        "m",
        missing_considerations,
        "Get key considerations that have been overlooked in the last message. "
        "Use '/m all' to process the whole conversation.",
    )
    registry.register(
        "s",
        summarize,
        "Summarize the last message. Use '/s all' to summarize the whole conversation.",
    )
    onboarding = OnboardingCommand(registry)

    start_handler = CommandHandler("start", onboarding)
    application.add_handler(start_handler)

    application.add_handler(MessageHandler(filters.ALL, record_messages))
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
