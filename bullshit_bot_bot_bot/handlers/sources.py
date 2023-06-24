import openai
from bullshit_bot_bot_bot.middleware import GenericMessage
from telegram import Update
from telegram.ext import ContextTypes

from langchain.chat_models import ChatOpenAI
from bullshit_bot_bot_bot.middleware import GenericMessage
from bullshit_bot_bot_bot.utils import print_messages
from middleware import telegram_updates_to_generic_thread

async def get_sources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = telegram_updates_to_generic_thread(context.chat_data.get("updates", []))

    response_text = get_topic_list(messages)

    # ... search google
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text,
    )

def get_topic_list(messages: list[GenericMessage]):
    model = ChatOpenAI()
    prompt = get_topic_extraction_prompt(messages)
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        functions=[
    {
      "name": "verify_claims",
      "description": "Verify that the claims are factual given a list of sentences",
      "parameters": {
        "type": "object",
        "properties": {
            "sentences": {
                "type": "array",
                "description": "A list of sentences to be verified. Maximum 5 sentences.",
                "items": {
                    "type": "string",
                    "description": "A single sentence that summarizes one of the key points of the news article."
                }
            }
        },
        "required": ["sentences"]
      }
    }
  ],
  function_call={
    "name": "verify_claims",
  }
    )
    print(chat_completion)
    arguments = chat_completion.choices[0].message.function_call.arguments
    # arguments is a string representation of {sentences: ["sentence1", "sentence2", ...]}
    arguments_as_dict = eval(arguments)
    content = arguments
    return content

def get_topic_extraction_prompt(messages: list[GenericMessage]):
    message_prompt_section = print_messages(messages)

    return f"""The following is a conversation taking place on a social media platform.
It may contain at least one message that is a news article or a summary of a news article.
Your task is to summarize the latest news article that is being discussed in the conversation into a list of sentences split by newlines.

Conversation:
{message_prompt_section}
"""
    