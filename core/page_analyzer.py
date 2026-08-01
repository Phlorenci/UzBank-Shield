"""
Payment page content analysis.

Fetches a page's HTML and looks for indicators that it collects
payment card information (card number, CVV, expiry fields), so
unverified domains asking for card details can be flagged more
strongly than a plain domain check alone would catch.
"""

import re

import requests
from bs4 import BeautifulSoup


CARD_FIELD_PATTERNS = [
    r"card[\s_-]?number",
    r"cardnumber",
    r"cc[\s_-]?number",
    r"credit[\s_-]?card",
    r"card[\s_-]?holder",
    r"expir",
    r"cvv",
    r"cvc",
    r"security[\s_-]?code",
]

REQUEST_TIMEOUT = 5


def analyze_payment_page(url):
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )

        if response.status_code >= 400:
            return {
                "analyzed": False,
                "requests_card_info": False,
                "matched_fields": [],
                "error": f"Page returned status {response.status_code}"
            }

        soup = BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as error:
        return {
            "analyzed": False,
            "requests_card_info": False,
            "matched_fields": [],
            "error": str(error)
        }

    matched_fields = _find_card_fields(soup)

    return {
        "analyzed": True,
        "requests_card_info": len(matched_fields) > 0,
        "matched_fields": matched_fields,
        "error": None
    }


def _find_card_fields(soup):

    matched = set()

    inputs = soup.find_all(["input", "label"])

    for tag in inputs:

        searchable_text = " ".join(filter(None, [
            tag.get("name", ""),
            tag.get("id", ""),
            tag.get("placeholder", ""),
            tag.get_text() if tag.name == "label" else ""
        ])).lower()

        if not searchable_text.strip():
            continue

        for pattern in CARD_FIELD_PATTERNS:

            if re.search(pattern, searchable_text):
                matched.add(pattern)
                break

    return sorted(matched)