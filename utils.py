from urllib.parse import urlparse
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
    
def extract_url_components(url):
    """
    Extract URL components using Python's built-in parser.
    """

    # Automatically add HTTPS if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    return {
        "original_url": url,
        "protocol": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment
    }