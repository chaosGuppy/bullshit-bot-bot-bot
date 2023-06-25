import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from bullshit_bot_bot_bot.middleware import (
    GenericMessage,
    telegram_updates_to_generic_thread,
    with_messages_processed,
)
from bullshit_bot_bot_bot.utils import print_messages, truncate_middle

SUMMARY_SYSTEM = """
You are an assistant that takes in a transcript of a conversation and generates a summary of it
""".strip()

SUMMARY_TEMPLATE = """
Here is the conversation to summarize:

\"\"\"
{transcript}
\"\"\"
""".strip()


@with_messages_processed
async def summarize(
    messages: list[GenericMessage], update: Update, context: ContextTypes.DEFAULT_TYPE
):
    printed_transcript = print_messages(messages)

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM},
            {
                "role": "user",
                "content": SUMMARY_TEMPLATE.format(
                    transcript=truncate_middle(
                        printed_transcript, 12000 - len(SUMMARY_TEMPLATE)
                    )
                ),
            },
        ],
    )
    content: str = chat_completion.choices[0].message.content.strip()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=content)
