# Gets User Input

from core.messages import get_message


def get_user_input(language="en"):
    """
    Ask the user for a URL.
    """

    while True:
        url = input(f"\n{get_message('prompt_enter_url', language)}").strip()

        if not url:
            print(get_message("empty_url", language))
            continue

        return url