import re
from email import message_from_string
from email.utils import parseaddr

from core.sms_analyzer import scan_message_patterns, detect_time_pressure, URLAnalyzer
from core.institution_lookup import get_known_institution_names
from core.similarity import get_domain
from core.messages import get_message


URL_PATTERN = re.compile(
    r"(https?://[^\s\"'<>]+)",
    re.IGNORECASE
)

HTML_LINK_PATTERN = re.compile(
    r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL
)


def assess_email_risk(analysis, language="en"):
    """
    Combine header analysis, hidden link detection, URL analysis,
    and scam patterns into a single overall verdict for the email.
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
                _("email_reason_link_risk").format(
                    url=url_result["url"],
                    level=level_word(url_level)
                )
            )

    sender_mismatch_triggered = analysis["sender_mismatch"]["mismatch_detected"]

    if sender_mismatch_triggered:
        for finding in analysis["sender_mismatch"]["findings"]:
            if finding["type"] == "sender_domain_mismatch":
                reasons.append(
                    _("email_reason_sender_mismatch").format(
                        institution=finding["claimed_institution"],
                        address=finding["from_address"]
                    )
                )
            elif finding["type"] == "reply_to_mismatch":
                reasons.append(
                    _("email_reason_reply_to_mismatch").format(
                        from_address=finding["from_address"],
                        reply_to=finding["reply_to_address"]
                    )
                )

    hidden_links_triggered = analysis["hidden_links"]["hidden_links_detected"]

    if hidden_links_triggered:
        for finding in analysis["hidden_links"]["findings"]:
            reasons.append(
                _("email_reason_hidden_link").format(
                    displayed=finding["displayed_text"],
                    actual=finding["actual_url"]
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

    time_pressure_triggered = analysis["time_pressure"]["detected"]

    if time_pressure_triggered:
        reasons.append(
            _("sms_reason_time_pressure").format(
                matches=", ".join(analysis["time_pressure"]["matches"])
            )
        )

    # Scoring: sender spoofing and hidden links are both strong,
    # low-false-positive signals — either alone is enough for HIGH
    if (
        sender_mismatch_triggered
        or hidden_links_triggered
        or pattern_categories >= 2
        or highest_url_level == "HIGH"
    ):
        level = "HIGH"
    elif (
        pattern_categories == 1
        or highest_url_level == "MEDIUM"
        or time_pressure_triggered
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


def _looks_like_raw_email(text):
    """
    Heuristic: does this look like real email source (has a From:
    header near the top) rather than casually pasted body text?
    """

    first_lines = text.strip().split("\n")[:15]
    header_pattern = re.compile(r"^(From|To|Subject|Reply-To|Return-Path):", re.IGNORECASE)

    return any(header_pattern.match(line) for line in first_lines)


def _extract_headers(text):
    """
    Parse real email headers using Python's email module.
    Returns sender/reply-to info, or None fields if parsing fails.
    """

    try:
        msg = message_from_string(text)

        from_name, from_address = parseaddr(msg.get("From", ""))
        reply_to_name, reply_to_address = parseaddr(msg.get("Reply-To", ""))

        return {
            "from_name": from_name or None,
            "from_address": from_address or None,
            "reply_to_address": reply_to_address or None,
            "subject": msg.get("Subject")
        }

    except Exception:
        return {
            "from_name": None,
            "from_address": None,
            "reply_to_address": None,
            "subject": None
        }


def detect_sender_mismatch(headers):
    findings = []

    from_name = (headers.get("from_name") or "").lower()
    from_address = headers.get("from_address") or ""
    reply_to = headers.get("reply_to_address") or ""

    if not from_name or not from_address:
        return {"mismatch_detected": False, "findings": findings}

    institutions = get_known_institution_names()

    for name, domains in institutions.items():
        if name in from_name:
            from_domain = from_address.split("@")[-1].lower() if "@" in from_address else ""
            matches_official = any(from_domain == d.lower() for d in domains)

            if not matches_official:
                findings.append({
                    "type": "sender_domain_mismatch",
                    "claimed_institution": name,
                    "from_address": from_address,
                    "official_domains": domains
                })

    if reply_to and reply_to.lower() != from_address.lower():
        findings.append({
            "type": "reply_to_mismatch",
            "from_address": from_address,
            "reply_to_address": reply_to
        })

    return {
        "mismatch_detected": len(findings) > 0,
        "findings": findings
    }


def detect_hidden_links(text):
    findings = []

    for href, display_text in HTML_LINK_PATTERN.findall(text):
        display_clean = re.sub(r"<[^>]+>", "", display_text).strip()

        # Only interesting if the displayed text itself looks like
        # a URL/domain — otherwise "click here" pointing anywhere
        # isn't inherently suspicious on its own
        looks_like_url = bool(re.match(r"^(https?://)?[\w.-]+\.\w{2,}", display_clean))

        if not looks_like_url:
            continue

        href_domain = get_domain(href if href.startswith(("http://", "https://")) else f"https://{href}")
        display_domain = get_domain(
            display_clean if display_clean.startswith(("http://", "https://")) else f"https://{display_clean}"
        )

        if href_domain != display_domain:
            findings.append({
                "displayed_text": display_clean,
                "actual_url": href
            })

    return {
        "hidden_links_detected": len(findings) > 0,
        "findings": findings
    }


def extract_urls(text):
    """
    Extract plain-text URLs from the email body (separate from
    HTML href extraction, to also catch plain-text emails).
    """

    matches = URL_PATTERN.findall(text)
    return list(dict.fromkeys(matches))  # dedupe, preserve order


def analyze_email(raw_text):
    has_headers = _looks_like_raw_email(raw_text)

    headers = _extract_headers(raw_text) if has_headers else None
    sender_mismatch = detect_sender_mismatch(headers) if headers else {"mismatch_detected": False, "findings": []}

    hidden_links = detect_hidden_links(raw_text)

    urls = extract_urls(raw_text)
    matched_patterns = scan_message_patterns(raw_text)
    time_pressure = detect_time_pressure(raw_text)

    url_results = []
    analyzer = URLAnalyzer()

    for url in urls:
        try:
            result = analyzer.analyze(url)
            url_results.append({"url": url, "analysis": result})
        except Exception as error:
            url_results.append({"url": url, "analysis": None, "error": str(error)})

    return {
        "has_headers": has_headers,
        "headers": headers,
        "sender_mismatch": sender_mismatch,
        "hidden_links": hidden_links,
        "urls": url_results,
        "matched_patterns": matched_patterns,
        "pattern_categories_matched": len(matched_patterns),
        "has_url": len(urls) > 0,
        "has_suspicious_patterns": len(matched_patterns) > 0,
        "time_pressure": time_pressure
    }