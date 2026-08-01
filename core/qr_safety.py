"""
Safety assessment for classified QR/barcode content.

Provides a risk-oriented summary for non-URL code types, since URLs
already get full analysis via URLAnalyzer.
"""


def assess_qr_safety(classification):
    """
    Given a classify_qr_content() result, return a safety summary:
        {"risk_level": "LOW" | "MEDIUM" | "INFO", "message": "..."}

    URL types are excluded — those should be routed through
    URLAnalyzer for full analysis instead of this lightweight check.
    """

    qr_type = classification["type"]
    details = classification["details"]

    if qr_type == "wifi":
        if not details.get("has_password"):
            return {
                "risk_level": "MEDIUM",
                "message": (
                    "This QR code connects to an open (no password) WiFi "
                    "network. Open networks can expose your traffic to "
                    "others on the same network. Only connect if you trust "
                    "the source of this code."
                )
            }
        return {
            "risk_level": "LOW",
            "message": (
                "This QR code connects to a password-protected WiFi "
                "network. Only connect if you trust the source of this code."
            )
        }

    if qr_type == "vcard":
        return {
            "risk_level": "LOW",
            "message": "This QR code contains contact information."
        }

    if qr_type == "email":
        return {
            "risk_level": "LOW",
            "message": "This QR code contains an email address."
        }

    if qr_type == "phone":
        return {
            "risk_level": "LOW",
            "message": "This QR code contains a phone number."
        }

    if qr_type == "crypto":
        return {
            "risk_level": "MEDIUM",
            "message": (
                "This QR code contains a cryptocurrency payment address. "
                "Cryptocurrency transactions cannot be reversed. Carefully "
                "verify the recipient before sending any funds."
            )
        }

    if qr_type == "emv_payment":
        merchant = details.get("merchant_name")
        is_dynamic = details.get("is_dynamic", False)

        dynamic_note = (
            "This is a one-time payment code generated for a specific "
            "transaction. "
            if is_dynamic
            else "This is a static payment code that may be reused for "
                 "multiple transactions. Static codes are more commonly "
                 "targeted for tampering (e.g. a sticker placed over a "
                 "merchant's real code). "
        )

        if merchant:
            merchant_note = f"This is a payment QR code for {merchant}. "
        else:
            merchant_note = (
                "This is a payment QR code. Merchant details could not be "
                "extracted from this code. "
            )

        return {
            "risk_level": "MEDIUM",
            "message": (
                f"{merchant_note}{dynamic_note}"
                "Confirm the merchant matches who you intend to pay "
                "before completing any transaction."
            )
        }

    if qr_type == "barcode":
        return {
            "risk_level": "INFO",
            "message": (
                f"This is a {details.get('symbology', 'standard')} barcode, "
                "typically used for product identification (retail items, "
                "inventory, etc.). Not usually a security concern on its own."
            )
        }

    if qr_type == "numeric_reference":
        return {
            "risk_level": "INFO",
            "message": (
                "This QR code contains a numeric code that may be a "
                "payment reference, account number, or similar identifier. "
                "The exact purpose could not be determined. If this was "
                "presented to you as a payment QR code, verify the amount "
                "and recipient through the payment app directly before "
                "confirming any transaction."
            )
        }
    
    return {
        "risk_level": "INFO",
        "message": (
            "This QR code contains plain text or an unrecognized format. "
            "No specific safety information is available for this content type."
        )
    }