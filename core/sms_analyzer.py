"""
SMS/message text scam analysis.

Given raw pasted message text, extracts any URLs for full analysis
via URLAnalyzer, and independently scans the message body for
scam language patterns (urgency, requests for sensitive info,
too-good-to-be-true claims, fake authority) across English,
Russian, and Uzbek.
"""

import json
import re
from pathlib import Path

from core.analyzer import URLAnalyzer


PATTERNS_PATH = Path("data/sms_scam_patterns.json")

URL_PATTERN = re.compile(
    r"(https?://[^\s]+)|(\bwww\.[^\s]+)|(\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)",
    re.IGNORECASE
)


def load_sms_patterns():
    """
    Load the SMS scam phrase pattern database.
    """

    if not PATTERNS_PATH.exists():
        raise FileNotFoundError(
            f"SMS scam pattern database not found: {PATTERNS_PATH}"
        )

    with open(PATTERNS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_urls(text):
    """
    Find URL-like substrings in free-form message text. Matches
    full http(s) URLs, www.-prefixed domains, and bare domains
    (e.g. "kapitalbank.uz") since SMS scams often omit the protocol.
    """

    matches = URL_PATTERN.findall(text)

    urls = []

    for match in matches:
        found = next((group for group in match if group), None)

        if found and found not in urls:
            urls.append(found)

    return urls


def scan_message_patterns(text, patterns=None):
    """
    Scan message text for scam-indicating phrases across all
    supported languages. Returns matched phrases grouped by category.
    """

    if patterns is None:
        patterns = load_sms_patterns()

    text_lower = text.lower()

    matched = {}

    for category, language_patterns in patterns["categories"].items():

        category_matches = []

        for language, phrases in language_patterns.items():

            for phrase in phrases:

                if phrase.lower() in text_lower:
                    category_matches.append(phrase)

        if category_matches:
            matched[category] = sorted(set(category_matches))

    return matched


def analyze_message(text):
    """
    Full SMS/message analysis: extract and analyze any URLs found,
    and scan the message body for scam language patterns.
    """

    urls = extract_urls(text)
    matched_patterns = scan_message_patterns(text)

    url_results = []

    analyzer = URLAnalyzer()

    for url in urls:
        try:
            result = analyzer.analyze(url)
            url_results.append({"url": url, "analysis": result})
        except Exception as error:
            url_results.append({"url": url, "analysis": None, "error": str(error)})

    return {
        "urls": url_results,
        "matched_patterns": matched_patterns,
        "pattern_categories_matched": len(matched_patterns),
        "has_url": len(urls) > 0,
        "has_suspicious_patterns": len(matched_patterns) > 0
    }

def assess_message_risk(analysis):
    """
    Combine URL analysis results and matched scam patterns into a
    single overall verdict for the message.

    Returns:
        {"level": "LOW" | "MEDIUM" | "HIGH", "reasons": ["...", ...]}
    """

    reasons = []
    highest_url_level = "LOW"

    level_rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

    for url_result in analysis["urls"]:

        if url_result.get("analysis") is None:
            continue

        url_level = url_result["analysis"]["level"]

        if level_rank[url_level] > level_rank[highest_url_level]:
            highest_url_level = url_level

        if url_level in ("MEDIUM", "HIGH"):
            reasons.append(
                f"Link '{url_result['url']}' scored {url_level} risk"
            )

    pattern_categories = analysis["pattern_categories_matched"]

    if pattern_categories > 0:
        category_names = ", ".join(analysis["matched_patterns"].keys())
        reasons.append(
            f"Message contains {pattern_categories} scam indicator "
            f"categor{'y' if pattern_categories == 1 else 'ies'}: {category_names}"
        )

    # Combine: multiple matched pattern categories alone is a strong
    # signal even without a risky URL, since many scam SMS have no
    # link at all (e.g. "reply with your PIN").
    if pattern_categories >= 2 or highest_url_level == "HIGH":
        level = "HIGH"
    elif pattern_categories == 1 or highest_url_level == "MEDIUM":
        level = "MEDIUM"
    else:
        level = "LOW"

    if not reasons:
        reasons.append("No suspicious links or scam language detected")

    return {
        "level": level,
        "reasons": reasons
    }