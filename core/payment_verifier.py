import json
from pathlib import Path

from core.similarity import get_domain, calculate_similarity, SIMILARITY_THRESHOLD


PAYMENT_DATABASE_PATH = Path("data/official_payment_processors.json")


def load_payment_processors():
    """
    Load the official payment processor database. Mirrors
    core.database.load_official_domains(), but for a separate
    file/category (Payme, Click, Uzcard, etc. rather than banks).
    """

    if not PAYMENT_DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Payment processor database not found: {PAYMENT_DATABASE_PATH}"
        )

    try:
        with open(PAYMENT_DATABASE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in payment processor database file.\n{error}"
        )

    required_fields = ["version", "country", "processors"]

    for field in required_fields:
        if field not in data:
            raise ValueError(
                f"Payment processor database is missing required field: '{field}'"
            )

    if not isinstance(data["processors"], list):
        raise ValueError(
            "'processors' must be a list."
        )

    return data


def _find_closest_processor_domain(url, database):
    """
    Same similarity-matching approach as core.similarity.find_closest_domain(),
    adapted for the processors list shape instead of banks.
    """

    user_domain = get_domain(url)

    best_match = None
    highest_similarity = 0

    for processor in database["processors"]:

        for official_domain in processor["domains"]:

            similarity = calculate_similarity(
                user_domain,
                official_domain
            )

            if similarity > highest_similarity:

                highest_similarity = similarity

                best_match = {
                    "processor": processor["name"],
                    "domain": official_domain,
                    "similarity": similarity
                }

    if highest_similarity < SIMILARITY_THRESHOLD:

        return {
            "processor": None,
            "domain": None,
            "similarity": highest_similarity,
            "matched": False
        }

    best_match["matched"] = True

    return best_match


def verify_payment_processor(url, database):
    """
    Check whether a URL matches a known official payment processor
    domain. Mirrors core.verifier.verify_domain()'s structure and
    typosquat-detection behavior, applied to payment processors
    instead of banks.
    """

    user_domain = get_domain(url)

    for processor in database["processors"]:

        for official_domain in processor["domains"]:

            if user_domain == official_domain.lower():

                return {
                    "verified": True,
                    "processor": processor["name"],
                    "official_domain": official_domain,
                    "closest_domain": official_domain,
                    "similarity": 100.0,
                    "possible_typosquatting": False
                }

    closest = _find_closest_processor_domain(url, database)

    if not closest["matched"]:

        return {
            "verified": False,
            "processor": None,
            "official_domain": None,
            "closest_domain": None,
            "similarity": closest["similarity"],
            "possible_typosquatting": False
        }

    return {
        "verified": False,
        "processor": closest["processor"],
        "official_domain": None,
        "closest_domain": closest["domain"],
        "similarity": closest["similarity"],
        "possible_typosquatting": True
    }