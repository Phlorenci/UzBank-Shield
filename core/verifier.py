#Official domain verification.

from urllib.parse import urlparse


def normalize_domain(domain):
    domain = domain.lower().strip()

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
                    "official_domain": official_domain,
                    "message": "Official bank domain verified"
                }

    return {
        "verified": False,
        "bank": "Unknown",
        "official_domain": None,
        "message": "Domain is not an official bank domain"
    }