"""
Safety assessment for classified QR/barcode content.

Provides a risk-oriented summary for non-URL code types, since URLs
already get full analysis via URLAnalyzer.
"""

from core.messages import get_message


def assess_qr_safety(classification, language="en"):
    """
    Given a classify_qr_content() result, return a safety summary:
        {"risk_level": "LOW" | "MEDIUM" | "INFO", "message": "..."}

    URL types are excluded — those should be routed through
    URLAnalyzer for full analysis instead of this lightweight check.
    """

    def _(key):
        return get_message(key, language)

    qr_type = classification["type"]
    details = classification["details"]

    if qr_type == "wifi":
        if not details.get("has_password"):
            return {"risk_level": "MEDIUM", "message": _("qr_safety_wifi_open")}
        return {"risk_level": "LOW", "message": _("qr_safety_wifi_secured")}

    if qr_type == "vcard":
        return {"risk_level": "LOW", "message": _("qr_safety_vcard")}

    if qr_type == "email":
        return {"risk_level": "LOW", "message": _("qr_safety_email")}

    if qr_type == "phone":
        return {"risk_level": "LOW", "message": _("qr_safety_phone")}

    if qr_type == "crypto":
        return {"risk_level": "MEDIUM", "message": _("qr_safety_crypto")}

    if qr_type == "emv_payment":
        merchant = details.get("merchant_name")
        is_dynamic = details.get("is_dynamic", False)

        dynamic_note = _("qr_safety_emv_dynamic") if is_dynamic else _("qr_safety_emv_static")

        if merchant:
            merchant_note = _("qr_safety_emv_with_merchant").format(merchant=merchant)
        else:
            merchant_note = _("qr_safety_emv_no_merchant")

        return {
            "risk_level": "MEDIUM",
            "message": f"{merchant_note}{dynamic_note}{_('qr_safety_emv_confirm')}"
        }

    if qr_type == "barcode":
        symbology = details.get("symbology", "standard")
        return {
            "risk_level": "INFO",
            "message": _("qr_safety_barcode").format(symbology=symbology)
        }

    if qr_type == "numeric_reference":
        return {"risk_level": "INFO", "message": _("qr_safety_numeric_reference")}

    return {"risk_level": "INFO", "message": _("qr_safety_unknown")}