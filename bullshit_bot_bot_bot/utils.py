from bullshit_bot_bot_bot.middleware import GenericMessage


def print_messages(messages: list[GenericMessage]):
    return "\n\n".join(
        [f'{message["username"]}: {message["text"]}' for message in messages]
    )
