# Risk scoring constants
KEYWORD_WEIGHT = 20
VERIFIED_DOMAIN_BONUS = -25
UNVERIFIED_DOMAIN_PENALTY = 25

LOW_THRESHOLD = 30
MEDIUM_THRESHOLD = 60


def calculate_risk_score(keywords, verification):
    score = 0

    # -------------------------
    # Keyword analysis
    # -------------------------

    score += len(keywords) * KEYWORD_WEIGHT

    # -------------------------
    # Official domain verification
    # -------------------------

    if verification["verified"]:
        score += VERIFIED_DOMAIN_BONUS
    else:
        score += UNVERIFIED_DOMAIN_PENALTY

    # -------------------------
    # Keep score between 0 and 100
    # -------------------------

    score = max(0, min(score, 100))

    # -------------------------
    # Risk level
    # -------------------------

    if score < LOW_THRESHOLD:
        level = "LOW"
    elif score < MEDIUM_THRESHOLD:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return score, level