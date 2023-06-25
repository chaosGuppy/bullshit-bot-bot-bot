from typing import TypedDict, Callable
from telegram import Update
from telegram.ext import ContextTypes


class GenericMessage(TypedDict):
    text: str
    username: str


def telegram_updates_to_generic_thread(telegram_updates: dict) -> list[GenericMessage]:
    result = []
    for update in telegram_updates:
        result.append(
            {
                "text": update["message"]["text"],
                "username": f'{update["message"]["from"]["first_name"]} '
                f'{update["message"]["from"].get("last_name", "")}',
            }
        )
    return result


def with_messages_processed(
    callback: Callable[[list[GenericMessage], Update, ContextTypes.DEFAULT_TYPE], None]
):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        updates = context.chat_data.get("updates", [])
        updates_for_chat = [
            u for u in updates if u["message"]["chat"]["id"] == update.effective_chat.id
        ]
        messages = telegram_updates_to_generic_thread(updates_for_chat)
        if not update.message.text.endswith("all"):
            messages = messages[-1:]
        await callback(messages, update, context)
        pass

    return wrapper
