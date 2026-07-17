# Extracts URL components
from urllib.parse import urlparse

"""
URL parsing module.
"""


def extract_url_components(url):
    """
    Extract URL components.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    return {
        "original_url": url,
        "protocol": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
    }