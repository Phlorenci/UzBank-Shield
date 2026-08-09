from core.email_analyzer import (
    _looks_like_raw_email,
    _extract_headers,
    detect_sender_mismatch,
    detect_hidden_links,
    extract_urls,
    analyze_email,
    assess_email_risk
)


def test_looks_like_raw_email_detects_headers():
    text = "From: test@example.com\nSubject: Hi\n\nBody text"
    assert _looks_like_raw_email(text) is True


def test_looks_like_raw_email_false_for_casual_text():
    text = "Hey, are we still meeting tomorrow?"
    assert _looks_like_raw_email(text) is False


def test_extract_headers_parses_from_and_reply_to():
    text = (
        "From: Kapitalbank Support <support@kapital-secure-alerts.com>\n"
        "Reply-To: scammer@totally-different.com\n"
        "Subject: Urgent\n\nBody"
    )

    headers = _extract_headers(text)

    assert headers["from_name"] == "Kapitalbank Support"
    assert headers["from_address"] == "support@kapital-secure-alerts.com"
    assert headers["reply_to_address"] == "scammer@totally-different.com"


def test_sender_mismatch_detected_for_spoofed_domain():
    headers = {
        "from_name": "Kapitalbank Support",
        "from_address": "support@kapital-secure-alerts.com",
        "reply_to_address": None
    }

    result = detect_sender_mismatch(headers)

    assert result["mismatch_detected"] is True
    assert result["findings"][0]["type"] == "sender_domain_mismatch"


def test_sender_mismatch_not_triggered_for_real_domain():
    headers = {
        "from_name": "Kapitalbank",
        "from_address": "info@kapitalbank.uz",
        "reply_to_address": "info@kapitalbank.uz"
    }

    result = detect_sender_mismatch(headers)

    assert result["mismatch_detected"] is False


def test_reply_to_mismatch_detected_even_with_legit_from_domain():
    headers = {
        "from_name": "Kapitalbank",
        "from_address": "info@kapitalbank.uz",
        "reply_to_address": "someone-else@gmail.com"
    }

    result = detect_sender_mismatch(headers)

    assert result["mismatch_detected"] is True
    assert any(f["type"] == "reply_to_mismatch" for f in result["findings"])


def test_detect_hidden_links_finds_mismatched_href():
    text = '<a href="https://evil-fake.uz/steal">kapitalbank.uz</a>'

    result = detect_hidden_links(text)

    assert result["hidden_links_detected"] is True
    assert result["findings"][0]["displayed_text"] == "kapitalbank.uz"
    assert result["findings"][0]["actual_url"] == "https://evil-fake.uz/steal"


def test_detect_hidden_links_ignores_non_url_display_text():
    text = '<a href="https://kapitalbank.uz">Click here</a>'

    result = detect_hidden_links(text)

    assert result["hidden_links_detected"] is False


def test_extract_urls_from_plain_text():
    text = "Visit https://kapitalbank.uz or https://payme.uz for details"

    urls = extract_urls(text)

    assert "https://kapitalbank.uz" in urls
    assert "https://payme.uz" in urls


def test_analyze_email_full_scam_with_headers():
    email_text = (
        "From: Kapitalbank Support <support@kapital-secure-alerts.com>\n"
        "Reply-To: scammer@totally-different.com\n"
        "Subject: Urgent\n\n"
        "Your account will be suspended within 24 hours. "
        "Verify now at https://kapita1bank.uz/verify"
    )

    result = analyze_email(email_text)

    assert result["has_headers"] is True
    assert result["sender_mismatch"]["mismatch_detected"] is True
    assert result["has_url"] is True
    assert result["has_suspicious_patterns"] is True


def test_analyze_email_honest_fallback_without_headers():
    email_text = "Congratulations! You've won a prize. Confirm your card number to claim it."

    result = analyze_email(email_text)

    assert result["has_headers"] is False
    assert result["sender_mismatch"]["mismatch_detected"] is False
    assert result["has_suspicious_patterns"] is True


def test_analyze_email_clean_casual_text():
    email_text = "Hi, just following up on the meeting notes from yesterday."

    result = analyze_email(email_text)

    assert result["has_url"] is False
    assert result["has_suspicious_patterns"] is False
    assert result["sender_mismatch"]["mismatch_detected"] is False


def test_assess_risk_high_for_sender_and_link_and_urgency():
    email_text = (
        "From: Kapitalbank Support <support@kapital-secure-alerts.com>\n"
        "Reply-To: scammer@totally-different.com\n"
        "Subject: Urgent\n\n"
        "Your account will be suspended within 24 hours. "
        "Verify now at https://kapita1bank.uz/verify"
    )

    analysis = analyze_email(email_text)
    risk = assess_email_risk(analysis)

    assert risk["level"] == "HIGH"
    assert len(risk["reasons"]) >= 3


def test_assess_risk_low_for_clean_email():
    email_text = "Hi, just following up on the meeting notes from yesterday."

    analysis = analyze_email(email_text)
    risk = assess_email_risk(analysis)

    assert risk["level"] == "LOW"


def test_assess_risk_low_for_verified_domain_link():
    email_text = "Reminder: your Click wallet monthly summary is ready at click.uz"

    analysis = analyze_email(email_text)
    risk = assess_email_risk(analysis)

    assert risk["level"] == "LOW"


def test_assess_risk_high_for_hidden_link_alone():
    email_text = '<a href="https://evil-fake.uz/steal">kapitalbank.uz</a>'

    analysis = analyze_email(email_text)
    risk = assess_email_risk(analysis)

    assert risk["level"] == "HIGH"