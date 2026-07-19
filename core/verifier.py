#Official domain verification.

from urllib.parse import urlparse


def normalize_domain(domain):
    """
    Normalize domains before comparison.
    """

    domain = domain.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def verify_domain(url, database):
    """
    Compare URL against official bank domains.

    Returns:
        dict
    """

    parsed = urlparse(url)

    domain = normalize_domain(parsed.netloc)

    for bank in database["banks"]:

        for official_domain in bank["domains"]:

            if domain == normalize_domain(official_domain):

                return {
                    "verified": True,
                    "bank": bank["name"],
                    "domain": official_domain
                }

    return {
        "verified": False,
        "bank": None,
        "domain": None
    }