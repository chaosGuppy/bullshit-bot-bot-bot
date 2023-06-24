from typing import TypedDict

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
