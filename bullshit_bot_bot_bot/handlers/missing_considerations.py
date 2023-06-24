from langchain.chat_models import ChatOpenAI
from bullshit_bot_bot_bot.middleware import GenericMessage
from bullshit_bot_bot_bot.utils import print_messages


def get_prompt(messages: list[GenericMessage]):
    message_prompt_section = print_messages(messages)

    return f"""The following is a conversation taking place on a social media platform.
Your task is to identify any key considerations that are relevant for the topic of the conversation,
but are being overlooked by the participants, in ways that lead to the conversation being unproductive or distorted.

Conversation:
{message_prompt_section}
---
"""


def get_missing_considerations(messages: list[GenericMessage]):
    model = ChatOpenAI()
    prompt = get_prompt(messages)
    return model.call_as_llm(prompt)
