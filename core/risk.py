def calculate_risk_score(
    keywords,
    verification,
    suspicious_tld
):
    score = 0

    # -----------------------------
    # Keyword analysis
    # -----------------------------
    score += len(keywords) * 15

    # -----------------------------
    # Official verification
    # -----------------------------
    if verification["verified"]:

        score -= 20

    # -----------------------------
    # Typosquatting detection
    # -----------------------------
    if verification["possible_typosquatting"]:

        score += 35

    # -----------------------------
    # Suspicious TLD
    # -----------------------------
    if suspicious_tld:

        score += 20

    # -----------------------------
    # Clamp score
    # -----------------------------
    score = max(0, min(score, 100))

    # -----------------------------
    # Risk level
    # -----------------------------
    if score < 30:

        level = "LOW"

    elif score < 60:

        level = "MEDIUM"

    else:

        level = "HIGH"

    return score, level