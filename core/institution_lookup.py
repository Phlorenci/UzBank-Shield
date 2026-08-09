from core.database import load_official_domains
from core.payment_verifier import load_payment_processors


def get_known_institution_names():
    """
    Build a lookup of known bank/payment processor names to their
    verified domains, for impersonation-mismatch detection.
    """

    institutions = {}

    bank_db = load_official_domains()
    for bank in bank_db["banks"]:
        institutions[bank["name"].lower()] = bank["domains"]

    payment_db = load_payment_processors()
    for processor in payment_db["processors"]:
        institutions[processor["name"].lower()] = processor["domains"]

    return institutions