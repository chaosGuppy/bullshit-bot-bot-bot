from bullshit_bot_bot_bot.middleware import GenericMessage


def print_messages(messages: list[GenericMessage]):
    return '\n\n'.join([f'{message["username"]}: {message["text"]}' for message in messages[-30:]])

# TODO actually write this, and a 'truncate_transcript' which truncates the messages, and the final included message
def truncate_middle(value: int, max_length: int):
    if len(value) <= max_length:
        return value
    
    truncated_str = "{ ...truncated }"
    remaining_length = max_length - len(truncated_str)

    return value[:(remaining_length // 2)] + truncated_str + value[-(remaining_length // 2):]