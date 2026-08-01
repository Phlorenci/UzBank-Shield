"""
QR code and barcode content classification.

Determines what kind of data a decoded code contains (URL, WiFi
credentials, contact card, payment QR, barcode, etc.) and extracts
a human-readable summary, so the app can route each type to
appropriate handling rather than assuming every code is a website.
"""

import re


def classify_qr_content(data, symbology="QRCODE"):
    """
    Classify decoded QR/barcode payload text.

    Returns a dict:
        {
            "type": "url" | "wifi" | "vcard" | "email" | "phone" |
                    "crypto" | "emv_payment" | "barcode" | "unknown",
            "summary": "<human-readable description>",
            "raw_data": "<original decoded string>",
            "details": {<type-specific extracted fields>}
        }
    """

    if symbology != "QRCODE":
        return {
            "type": "barcode",
            "summary": f"{symbology} barcode",
            "raw_data": data,
            "details": {"symbology": symbology, "value": data}
        }

    if data.startswith(("http://", "https://")):
        return {
            "type": "url",
            "summary": "Website link",
            "raw_data": data,
            "details": {"url": data}
        }

    if data.startswith("WIFI:"):
        return _classify_wifi(data)

    if data.startswith("BEGIN:VCARD"):
        return _classify_vcard(data)

    if data.startswith("mailto:"):
        email = data[len("mailto:"):].split("?")[0]
        return {
            "type": "email",
            "summary": "Email address",
            "raw_data": data,
            "details": {"email": email}
        }

    if data.startswith("tel:"):
        phone = data[len("tel:"):]
        return {
            "type": "phone",
            "summary": "Phone number",
            "raw_data": data,
            "details": {"phone": phone}
        }

    if data.startswith(("bitcoin:", "ethereum:", "litecoin:")):
        scheme = data.split(":")[0]
        address = data.split(":")[1].split("?")[0] if ":" in data else data
        return {
            "type": "crypto",
            "summary": f"{scheme.capitalize()} payment address",
            "raw_data": data,
            "details": {"scheme": scheme, "address": address}
        }

    if _looks_like_emv_payment(data):
        return _classify_emv_payment(data)

    if _looks_like_numeric_reference(data):
        return {
            "type": "numeric_reference",
            "summary": "Possible payment or reference number",
            "raw_data": data,
            "details": {"value": data, "length": len(data)}
        }

    return {
        "type": "unknown",
        "summary": "Plain text or unrecognized format",
        "raw_data": data,
        "details": {}
    }


def _classify_wifi(data):
    """
    Parse WIFI:T:<type>;S:<ssid>;P:<password>;; format.
    """

    fields = {}

    pattern = r"([A-Z]):((?:[^\\;]|\\.)*)"
    matches = re.findall(pattern, data)

    for key, value in matches:
        fields[key] = value.replace("\\;", ";").replace("\\,", ",").replace("\\\\", "\\")

    ssid = fields.get("S", "Unknown network")
    security = fields.get("T", "Unknown")

    return {
        "type": "wifi",
        "summary": f"WiFi network: {ssid}",
        "raw_data": data,
        "details": {
            "ssid": ssid,
            "security": security,
            "has_password": bool(fields.get("P"))
        }
    }


def _classify_vcard(data):
    """
    Extract basic fields from a VCARD payload.
    """

    name_match = re.search(r"FN:(.+)", data)
    tel_match = re.search(r"TEL[^:]*:(.+)", data)
    email_match = re.search(r"EMAIL[^:]*:(.+)", data)

    return {
        "type": "vcard",
        "summary": "Contact card",
        "raw_data": data,
        "details": {
            "name": name_match.group(1).strip() if name_match else "Unknown",
            "phone": tel_match.group(1).strip() if tel_match else None,
            "email": email_match.group(1).strip() if email_match else None
        }
    }


def _looks_like_emv_payment(data):
    """
    EMV QR Code Payment strings (used by Toss, Alipay, WeChat Pay,
    and many other mobile payment apps worldwide) follow a
    Tag-Length-Value structure and always start with tag "00" set
    to payload format indicator "01".
    """

    return (
        data.startswith("000201")
        and data[-4:].isdigit()  # CRC checksum, always 4 hex-like digits
        and len(data) > 20
    )

def _looks_like_numeric_reference(data):
    """
    Numeric-only strings of meaningful length that don't match any
    other known format. Could be a partial/regional payment payload,
    account number, or reference code — flagged as noteworthy rather
    than a confident classification, since there's no reliable way
    to distinguish these from other numeric identifiers.
    """

    return data.isdigit() and len(data) >= 10

def _classify_emv_payment(data):
    """
    Parse the top-level Tag-Length-Value fields of an EMV QR
    payment string. Doesn't fully decode every possible tag —
    just extracts the fields useful for a safety summary.

    Note: merchant name/city (tags 59/60) follow the international
    EMVCo spec, but some regional payment networks (e.g. Korean
    domestic QR payment systems) encode merchant identity via a
    bank/PG lookup instead, so these fields may be unavailable even
    though the QR is correctly identified as a payment code.
    """

    fields = _parse_tlv(data)

    merchant_name = fields.get("59")
    merchant_city = fields.get("60", "")
    country = fields.get("58", "")

    is_dynamic = fields.get("01") == "12"

    if merchant_name:
        summary = f"Payment QR code ({merchant_name})"
    else:
        summary = "Payment QR code"

    return {
        "type": "emv_payment",
        "summary": summary,
        "raw_data": data,
        "details": {
            "merchant_name": merchant_name,
            "merchant_city": merchant_city,
            "country": country,
            "is_dynamic": is_dynamic
        }
    }


def _parse_tlv(data):
    """
    Parse EMV QR's Tag-Length-Value encoding: each field is a
    2-digit tag, 2-digit length, then that many characters of value.
    """

    fields = {}
    i = 0

    while i < len(data) - 4:

        tag = data[i:i + 2]
        length_str = data[i + 2:i + 4]

        if not length_str.isdigit():
            break

        length = int(length_str)
        value = data[i + 4:i + 4 + length]

        fields[tag] = value
        i += 4 + length

    return fields