import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from bullshit_bot_bot_bot.middleware import telegram_updates_to_generic_thread
from bullshit_bot_bot_bot.utils import print_messages

SUMMARY_TEMPLATE = """
Here is the summary of the conversation:\n\n{summary}
""".strip()


async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = telegram_updates_to_generic_thread(context.chat_data["updates"])
    printed_messages = print_messages(messages)
    
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that takes in a transcript of a conversation and generates a summary of it",
            },
            {"role": "user", "content": SUMMARY_TEMPLATE.format(summary=printed_messages)},
        ],
    )
    content = chat_completion.choices[0].message.content

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=content
    )
