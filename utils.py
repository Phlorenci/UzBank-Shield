"""
Utility functions for UzBank Shield
"""

def get_user_input():
    """
    Ask the user to enter a URL.
    Returns a cleaned string.
    """

    while True:
        url = input("\n Enter a website URL: ").strip()

        if url == "":
            print(" URL cannot be empty. Please try again.")
            continue

        return url