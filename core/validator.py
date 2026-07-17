# Validates URLs
import re
from urllib.parse import urlparse

"""
URL validation module.
"""


def validate_url(url):
    """
    Validate user URL.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False

    if not parsed.netloc:
        return False

    domain_pattern = re.compile(
        r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    )

    return bool(domain_pattern.match(parsed.netloc))