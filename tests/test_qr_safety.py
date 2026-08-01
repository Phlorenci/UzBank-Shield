from core.qr_classifier import classify_qr_content
from core.qr_safety import assess_qr_safety


def test_safety_open_wifi_is_medium_risk():
    classification = classify_qr_content("WIFI:T:nopass;S:OpenNetwork;;")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "MEDIUM"


def test_safety_password_wifi_is_low_risk():
    classification = classify_qr_content("WIFI:T:WPA;S:Home;P:secret;;")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "LOW"


def test_safety_vcard_is_low_risk():
    classification = classify_qr_content("BEGIN:VCARD\nFN:Test\nEND:VCARD")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "LOW"


def test_safety_crypto_is_medium_risk():
    classification = classify_qr_content("bitcoin:1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "MEDIUM"
    assert "cannot be reversed" in result["message"]


def test_safety_emv_payment_with_merchant_name():
    emv_sample = "00020101021229370016A0000006770101110113005500011048340142291373"
    classification = classify_qr_content(emv_sample)
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "MEDIUM"
    assert "Merchant details could not be extracted" in result["message"]


def test_safety_barcode_is_info_level():
    classification = classify_qr_content("012345678905", symbology="EAN13")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "INFO"


def test_safety_numeric_reference_is_info_level():
    classification = classify_qr_content("705500011048340142291591")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "INFO"


def test_safety_unknown_is_info_level():
    classification = classify_qr_content("random plain text")
    result = assess_qr_safety(classification)

    assert result["risk_level"] == "INFO"