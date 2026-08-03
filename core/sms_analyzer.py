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
from core.database import load_official_domains
from core.payment_verifier import load_payment_processors
from core.similarity import get_domain
from core.messages import get_message

PATTERNS_PATH = Path("data/sms_scam_patterns.json")

URL_PATTERN = re.compile(
    r"(https?://[^\s]+)|(\bwww\.[^\s]+)|(\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)",
    re.IGNORECASE
)

TIME_PRESSURE_PATTERN = re.compile(
    r"\b(\d{1,3})\s*(hour|hours|minute|minutes|day|days|soat|kun|daqiqa|час|часа|часов|минут|минуты|день|дня|дней)\b",
    re.IGNORECASE
)

IMPERATIVE_VERBS = [
    "verify", "confirm", "click", "reply", "call", "update", "login", "log in",
    "подтвердите", "перейдите", "позвоните", "войдите", "нажмите",
    "tasdiqlang", "kiring", "qo'ng'iroq qiling", "bosing"
]


def _get_known_institution_names():
    """
    Build a lookup of known bank/payment processor names to their
    verified domains, for impersonation-mismatch detection.
    """

    institutions = {}

    bank_db = load_official_domains()
    for bank in bank_db["banks"]:
        institutions[bank["name"].lower()] = bank["domains"]

    payment_db = load_payment_processors()
    for processor in payment_db["processors"]:
        institutions[processor["name"].lower()] = processor["domains"]

    return institutions

def detect_institution_impersonation(text, urls):
    """
    Check whether the message names a real bank/payment processor,
    but any link present doesn't match that institution's actual
    verified domain. This is a strong signal independent of exact
    scam phrasing — it catches "This is Kapitalbank, verify at
    kapita1-secure.uz" regardless of how the rest of the message
    is worded.
    """

    text_lower = text.lower()
    institutions = _get_known_institution_names()

    mentioned = []

    for name, domains in institutions.items():
        if name in text_lower:
            mentioned.append((name, domains))

    if not mentioned:
        return {"impersonation_detected": False, "details": []}

    findings = []

    for name, official_domains in mentioned:

        for url in urls:
            url_domain = get_domain(url if url.startswith(("http://", "https://")) else f"https://{url}")

            matches_official = any(
                url_domain == official.lower() for official in official_domains
            )

            if not matches_official:
                findings.append({
                    "claimed_institution": name,
                    "official_domains": official_domains,
                    "actual_url": url,
                    "actual_domain": url_domain
                })

    return {
        "impersonation_detected": len(findings) > 0,
        "details": findings
    }


def detect_time_pressure(text):
    """
    Regex-based detection of urgency framed around a time limit
    (e.g. "3 hours", "24 soat", "48 часов"), independent of the
    exact surrounding phrase used.
    """

    matches = TIME_PRESSURE_PATTERN.findall(text)

    return {
        "detected": len(matches) > 0,
        "matches": [f"{number} {unit}" for number, unit in matches]
    }


def detect_structural_indicators(text, has_url):
    """
    Looks for combinations of weaker signals that together suggest
    a phishing SMS shape, even without any specific trigger phrase:
    a link present, an imperative/action verb, and a short message
    (scam SMS are typically brief and direct).
    """

    text_lower = text.lower()

    has_imperative = any(verb in text_lower for verb in IMPERATIVE_VERBS)
    is_short = len(text.strip()) < 200

    score = sum([has_url, has_imperative, is_short])

    return {
        "has_imperative_verb": has_imperative,
        "is_short_message": is_short,
        "structural_score": score,
        # 3/3 signals together is a meaningfully stronger indicator
        # than any one alone
        "suspicious_shape": score >= 3
    }


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
    impersonation = detect_institution_impersonation(text, urls)
    time_pressure = detect_time_pressure(text)
    structural = detect_structural_indicators(text, has_url=len(urls) > 0)

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
        "has_suspicious_patterns": len(matched_patterns) > 0,
        "impersonation": impersonation,
        "time_pressure": time_pressure,
        "structural": structural
    }

def assess_message_risk(analysis, language="en"):
    """
    Combine URL analysis, matched scam patterns, and structural
    detections into a single overall verdict for the message.
    """

    def _(key):
        return get_message(key, language)

    def level_word(level):
        return get_message(f"risk_level_{level.lower()}", language)

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
                _("sms_reason_link_risk").format(
                    url=url_result["url"],
                    level=level_word(url_level)
                )
            )

    pattern_categories = analysis["pattern_categories_matched"]

    if pattern_categories > 0:
        category_names = ", ".join(analysis["matched_patterns"].keys())

        if pattern_categories == 1:
            reasons.append(
                _("sms_reason_pattern_count_singular").format(categories=category_names)
            )
        else:
            reasons.append(
                _("sms_reason_pattern_count").format(
                    count=pattern_categories,
                    categories=category_names
                )
            )

    impersonation_triggered = analysis["impersonation"]["impersonation_detected"]

    if impersonation_triggered:
        for finding in analysis["impersonation"]["details"]:
            reasons.append(
                _("sms_reason_impersonation").format(
                    institution=finding["claimed_institution"],
                    domain=finding["actual_domain"]
                )
            )

    time_pressure_triggered = analysis["time_pressure"]["detected"]

    if time_pressure_triggered:
        reasons.append(
            _("sms_reason_time_pressure").format(
                matches=", ".join(analysis["time_pressure"]["matches"])
            )
        )

    structural_triggered = analysis["structural"]["suspicious_shape"]

    if structural_triggered:
        reasons.append(_("sms_reason_structural"))

    if impersonation_triggered or pattern_categories >= 2 or highest_url_level == "HIGH":
        level = "HIGH"
    elif (
        pattern_categories == 1
        or highest_url_level == "MEDIUM"
        or time_pressure_triggered
        or structural_triggered
    ):
        level = "MEDIUM"
    else:
        level = "LOW"

    if not reasons:
        reasons.append(_("sms_reason_none"))

    return {
        "level": level,
        "reasons": reasons
    }