from urllib.parse import urlparse

import requests


def check_https(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    protocol = parsed.scheme.upper()

    try:

        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True
        )

        reachable = True
        status_code = response.status_code

    except requests.RequestException:

        reachable = False
        status_code = None

    return {
        "protocol": protocol,
        "https": protocol == "HTTPS",
        "reachable": reachable,
        "status_code": status_code
    }