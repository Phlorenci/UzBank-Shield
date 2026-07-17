# Scans for phishing indicators
import json
from pathlib import Path

"""
Phishing keyword detection module.
"""


KEYWORD_FILE = Path(__file__).parent.parent / "data" / "phishing_keywords.json"


def load_keywords():
    """
    Load phishing keywords from JSON.
    """

    with open(KEYWORD_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def scan_for_keywords(components):
    """
    Scan URL components for suspicious keywords.
    """

    keywords = load_keywords()

    text = " ".join([
        components["domain"],
        components["path"],
        components["query"]
    ]).lower()

    detected = []

    for keyword in keywords:
        if keyword.lower() in text:
            detected.append(keyword)

    return sorted(set(detected))