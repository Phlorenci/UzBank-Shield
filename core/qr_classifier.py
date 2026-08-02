"""
QR code and barcode content classification.

Determines what kind of data a decoded code contains (URL, WiFi
credentials, contact card, payment QR, barcode, etc.) and extracts
a human-readable summary, so the app can route each type to
appropriate handling rather than assuming every code is a website.
"""

import re

from core.messages import get_message


def classify_qr_content(data, symbology="QRCODE", language="en"):
    """
    Classify decoded QR/barcode payload text.

    Returns a dict:
        {
            "type": "url" | "wifi" | "vcard" | "email" | "phone" |
                    "crypto" | "emv_payment" | "barcode" |
                    "numeric_reference" | "unknown",
            "summary": "<human-readable description, in the given language>",
            "raw_data": "<original decoded string>",
            "details": {<type-specific extracted fields>}
        }
    """

    def _(key):
        return get_message(key, language)

    if symbology != "QRCODE":
        return {
            "type": "barcode",
            "summary": _("qr_type_barcode").format(symbology=symbology),
            "raw_data": data,
            "details": {"symbology": symbology, "value": data}
        }

    if data.startswith(("http://", "https://")):
        return {
            "type": "url",
            "summary": _("qr_type_url"),
            "raw_data": data,
            "details": {"url": data}
        }

    if data.startswith("WIFI:"):
        return _classify_wifi(data, language)

    if data.startswith("BEGIN:VCARD"):
        return _classify_vcard(data, language)

    if data.startswith("mailto:"):
        email = data[len("mailto:"):].split("?")[0]
        return {
            "type": "email",
            "summary": _("qr_type_email"),
            "raw_data": data,
            "details": {"email": email}
        }

    if data.startswith("tel:"):
        phone = data[len("tel:"):]
        return {
            "type": "phone",
            "summary": _("qr_type_phone"),
            "raw_data": data,
            "details": {"phone": phone}
        }

    if data.startswith(("bitcoin:", "ethereum:", "litecoin:")):
        scheme = data.split(":")[0]
        address = data.split(":")[1].split("?")[0] if ":" in data else data
        return {
            "type": "crypto",
            "summary": _("qr_type_crypto_payment").format(scheme=scheme.capitalize()),
            "raw_data": data,
            "details": {"scheme": scheme, "address": address}
        }

    if _looks_like_emv_payment(data):
        return _classify_emv_payment(data, language)

    if _looks_like_numeric_reference(data):
        return {
            "type": "numeric_reference",
            "summary": _("qr_type_numeric_reference"),
            "raw_data": data,
            "details": {"value": data, "length": len(data)}
        }

    return {
        "type": "unknown",
        "summary": _("qr_type_unknown"),
        "raw_data": data,
        "details": {}
    }


def _classify_wifi(data, language="en"):
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

    summary = f"{get_message('qr_type_wifi', language)}: {ssid}"

    return {
        "type": "wifi",
        "summary": summary,
        "raw_data": data,
        "details": {
            "ssid": ssid,
            "security": security,
            "has_password": bool(fields.get("P"))
        }
    }


def _classify_vcard(data, language="en"):
    """
    Extract basic fields from a VCARD payload.
    """

    name_match = re.search(r"FN:(.+)", data)
    tel_match = re.search(r"TEL[^:]*:(.+)", data)
    email_match = re.search(r"EMAIL[^:]*:(.+)", data)

    return {
        "type": "vcard",
        "summary": get_message("qr_type_vcard", language),
        "raw_data": data,
        "details": {
            "name": name_match.group(1).strip() if name_match else "Unknown",
            "phone": tel_match.group(1).strip() if tel_match else None,
            "email": email_match.group(1).strip() if email_match else None
        }
    }


def _looks_like_emv_payment(data):
    """
    EMV QR Code Payment strings follow a Tag-Length-Value structure
    and always start with tag "00" set to payload format indicator "01".
    """

    return (
        data.startswith("000201")
        and data[-4:].isdigit()
        and len(data) > 20
    )


def _looks_like_numeric_reference(data):
    """
    Numeric-only strings of meaningful length that don't match any
    other known format.
    """

    return data.isdigit() and len(data) >= 10


def _classify_emv_payment(data, language="en"):
    """
    Parse the top-level Tag-Length-Value fields of an EMV QR
    payment string.
    """

    fields = _parse_tlv(data)

    merchant_name = fields.get("59")
    merchant_city = fields.get("60", "")
    country = fields.get("58", "")

    is_dynamic = fields.get("01") == "12"

    if merchant_name:
        summary = get_message("qr_type_emv_payment_with_merchant", language).format(merchant=merchant_name)
    else:
        summary = get_message("qr_type_emv_payment", language)

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
    Parse EMV QR's Tag-Length-Value encoding.
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