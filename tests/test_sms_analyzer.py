from core.sms_analyzer import (
    extract_urls,
    scan_message_patterns,
    analyze_message,
    assess_message_risk,
    detect_institution_impersonation,
    detect_time_pressure,
    detect_structural_indicators
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

def test_impersonation_detected_when_domain_mismatches():
    text = "This is Kapitalbank. Please confirm your details at kapital-verify.uz"
    urls = ["kapital-verify.uz"]

    result = detect_institution_impersonation(text, urls)

    assert result["impersonation_detected"] is True
    assert result["details"][0]["claimed_institution"] == "kapitalbank"


def test_impersonation_not_triggered_for_real_domain():
    text = "This is Kapitalbank. Log in at kapitalbank.uz"
    urls = ["kapitalbank.uz"]

    result = detect_institution_impersonation(text, urls)

    assert result["impersonation_detected"] is False


def test_impersonation_not_triggered_when_no_institution_named():
    text = "Check this link: some-random-site.uz"
    urls = ["some-random-site.uz"]

    result = detect_institution_impersonation(text, urls)

    assert result["impersonation_detected"] is False


def test_time_pressure_detects_novel_phrasing():
    text = "Your card access ends in 3 hours unless you act."
    result = detect_time_pressure(text)

    assert result["detected"] is True
    assert "3 hours" in result["matches"]


def test_time_pressure_detects_russian_units():
    text = "Доступ закроется через 5 часов."
    result = detect_time_pressure(text)

    assert result["detected"] is True


def test_time_pressure_not_triggered_on_clean_text():
    text = "Hey, are we still meeting for lunch tomorrow?"
    result = detect_time_pressure(text)

    assert result["detected"] is False


def test_structural_indicators_flag_short_link_imperative_combo():
    text = "Verify now: suspicious-link.uz"
    result = detect_structural_indicators(text, has_url=True)

    assert result["suspicious_shape"] is True


def test_structural_indicators_not_triggered_for_long_casual_message():
    text = (
        "Hey, I was thinking about our conversation yesterday and wanted "
        "to follow up on a few things we discussed regarding the weekend plans."
    )
    result = detect_structural_indicators(text, has_url=False)

    assert result["suspicious_shape"] is False