from core.sms_analyzer import (
    extract_urls,
    scan_message_patterns,
    analyze_message,
    assess_message_risk
)


def test_extract_url_with_protocol():
    text = "Check this out: https://kapitalbank.uz/login"
    urls = extract_urls(text)

    assert "https://kapitalbank.uz/login" in urls


def test_extract_bare_domain_without_protocol():
    text = "Verify now at kapita1bank.uz to continue"
    urls = extract_urls(text)

    assert "kapita1bank.uz" in urls


def test_extract_multiple_urls():
    text = "Visit kapitalbank.uz or https://payme.uz for details"
    urls = extract_urls(text)

    assert len(urls) == 2


def test_extract_no_urls_in_plain_text():
    text = "Hey, are we still meeting for lunch tomorrow?"
    urls = extract_urls(text)

    assert urls == []


def test_scan_patterns_detects_english_urgency():
    text = "Your account will be suspended within 24 hours. Verify now."
    matched = scan_message_patterns(text)

    assert "urgency" in matched


def test_scan_patterns_detects_russian_urgency():
    text = "Ваша карта заблокирована. Подтвердите сейчас."
    matched = scan_message_patterns(text)

    assert "urgency" in matched


def test_scan_patterns_detects_uzbek_urgency():
    text = "Sizning hisobingiz 24 soat ichida bloklanadi."
    matched = scan_message_patterns(text)

    assert "urgency" in matched


def test_scan_patterns_detects_sensitive_info_request():
    text = "Please reply with your PIN to confirm your identity."
    matched = scan_message_patterns(text)

    assert "sensitive_info_request" in matched


def test_scan_patterns_detects_too_good_to_be_true():
    text = "Congratulations! You've won a prize. Claim your free gift now."
    matched = scan_message_patterns(text)

    assert "too_good_to_be_true" in matched


def test_scan_patterns_no_match_on_clean_text():
    text = "Hey, are we still meeting for lunch tomorrow?"
    matched = scan_message_patterns(text)

    assert matched == {}


def test_analyze_message_full_scam():
    text = "URGENT: Your account will be suspended within 24 hours. Verify now at kapita1bank.uz"
    result = analyze_message(text)

    assert result["has_url"] is True
    assert result["has_suspicious_patterns"] is True
    assert result["urls"][0]["analysis"]["verification"]["possible_typosquatting"] is True


def test_analyze_message_clean():
    text = "Hey, are we still meeting for lunch tomorrow?"
    result = analyze_message(text)

    assert result["has_url"] is False
    assert result["has_suspicious_patterns"] is False


def test_assess_risk_high_for_typosquat_and_urgency():
    text = "URGENT: Your account will be suspended within 24 hours. Verify now at kapita1bank.uz"
    analysis = analyze_message(text)
    risk = assess_message_risk(analysis)

    assert risk["level"] == "HIGH"
    assert len(risk["reasons"]) >= 2


def test_assess_risk_low_for_clean_message():
    text = "Hey, are we still meeting for lunch tomorrow?"
    analysis = analyze_message(text)
    risk = assess_message_risk(analysis)

    assert risk["level"] == "LOW"


def test_assess_risk_medium_for_single_pattern_category_no_url():
    text = "Please reply with your PIN to confirm your identity."
    analysis = analyze_message(text)
    risk = assess_message_risk(analysis)

    assert risk["level"] == "MEDIUM"


def test_assess_risk_high_for_multiple_pattern_categories():
    text = (
        "URGENT NOTICE: Your account will be suspended within 24 hours. "
        "You've won a prize! Reply with your PIN to claim your free gift."
    )
    analysis = analyze_message(text)
    risk = assess_message_risk(analysis)

    assert risk["level"] == "HIGH"


def test_analyze_message_with_verified_domain_is_low_risk():
    text = "Your delivery has arrived. Track it at kapitalbank.uz for account info."
    analysis = analyze_message(text)
    risk = assess_message_risk(analysis)

    assert analysis["has_url"] is True
    assert analysis["urls"][0]["analysis"]["verification"]["verified"] is True
    assert risk["level"] == "LOW"