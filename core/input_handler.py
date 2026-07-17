# Gets User Input

def get_user_input():
    """
    Ask the user for a URL.
    """

    while True:
        url = input("\nEnter a website URL: ").strip()

        if not url:
            print("URL cannot be empty.")
            continue

        return url