from core.qr_classifier import classify_qr_content


def test_classify_url():
    result = classify_qr_content("https://kapitalbank.uz")

    assert result["type"] == "url"
    assert result["details"]["url"] == "https://kapitalbank.uz"


def test_classify_wifi_with_password():
    result = classify_qr_content("WIFI:T:WPA;S:CafeWiFi;P:password123;;")

    assert result["type"] == "wifi"
    assert result["details"]["ssid"] == "CafeWiFi"
    assert result["details"]["has_password"] is True


def test_classify_wifi_open_network():
    result = classify_qr_content("WIFI:T:nopass;S:OpenNetwork;;")

    assert result["type"] == "wifi"
    assert result["details"]["ssid"] == "OpenNetwork"
    assert result["details"]["has_password"] is False


def test_classify_vcard():
    vcard = "BEGIN:VCARD\nVERSION:3.0\nFN:John Doe\nTEL:+998901234567\nEMAIL:john@example.com\nEND:VCARD"
    result = classify_qr_content(vcard)

    assert result["type"] == "vcard"
    assert result["details"]["name"] == "John Doe"
    assert result["details"]["phone"] == "+998901234567"
    assert result["details"]["email"] == "john@example.com"


def test_classify_email():
    result = classify_qr_content("mailto:test@example.com")

    assert result["type"] == "email"
    assert result["details"]["email"] == "test@example.com"


def test_classify_phone():
    result = classify_qr_content("tel:+998901234567")

    assert result["type"] == "phone"
    assert result["details"]["phone"] == "+998901234567"


def test_classify_crypto_bitcoin():
    result = classify_qr_content("bitcoin:1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

    assert result["type"] == "crypto"
    assert result["details"]["scheme"] == "bitcoin"
    assert result["details"]["address"] == "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"


def test_classify_emv_payment_full_header():
    emv_sample = "00020101021229370016A0000006770101110113005500011048340142291373"
    result = classify_qr_content(emv_sample)

    assert result["type"] == "emv_payment"
    assert result["details"]["is_dynamic"] is True


def test_classify_emv_payment_missing_merchant_name():
    emv_sample = "00020101021229370016A0000006770101110113005500011048340142291373"
    result = classify_qr_content(emv_sample)

    # This sample doesn't encode tags 59/60, so merchant name should
    # be None rather than a fabricated placeholder
    assert result["details"]["merchant_name"] is None


def test_classify_numeric_reference_fallback():
    result = classify_qr_content("705500011048340142291591")

    assert result["type"] == "numeric_reference"
    assert result["details"]["value"] == "705500011048340142291591"


def test_classify_short_numeric_string_is_unknown():
    # Below the length threshold for a "reference number" guess
    result = classify_qr_content("12345")

    assert result["type"] == "unknown"


def test_classify_plain_text_unknown():
    result = classify_qr_content("just some random text")

    assert result["type"] == "unknown"


def test_classify_barcode_symbology():
    result = classify_qr_content("012345678905", symbology="EAN13")

    assert result["type"] == "barcode"
    assert result["details"]["symbology"] == "EAN13"
    assert result["details"]["value"] == "012345678905"