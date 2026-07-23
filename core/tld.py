from urllib.parse import urlparse


SUSPICIOUS_TLDS = {
    ".xyz",
    ".top",
    ".click",
    ".work",
    ".shop",
    ".site",
    ".online",
    ".buzz",
    ".monster",
    ".zip",
    ".review"
}


def get_tld(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    domain = urlparse(url).netloc.lower()

    if "." not in domain:
        return ""

    return "." + domain.split(".")[-1]


def is_suspicious_tld(url):
    return get_tld(url) in SUSPICIOUS_TLDS