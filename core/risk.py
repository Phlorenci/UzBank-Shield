def calculate_risk_score(
    keywords,
    verification,
    suspicious_tld,
    connection
):
    score = 0

    # ---------------------------------
    # Phishing keywords
    # ---------------------------------

    score += len(keywords) * 15

    # ---------------------------------
    # Official verification
    # ---------------------------------

    if verification["verified"]:

        score -= 20

    # ---------------------------------
    # Possible bank impersonation
    # ---------------------------------

    if verification["possible_typosquatting"]:

        score += 35

    # ---------------------------------
    # Suspicious TLD
    # ---------------------------------

    if suspicious_tld:

        score += 20

    # ---------------------------------
    # HTTP instead of HTTPS
    # ---------------------------------

    if not connection["https"]:

        score += 15

    # ---------------------------------
    # Website unreachable
    # ---------------------------------

    if not connection["reachable"]:

        score += 10

    # ---------------------------------
    # Clamp score
    # ---------------------------------

    score = max(0, min(score, 100))

    # ---------------------------------
    # Risk Level
    # ---------------------------------

    if score < 30:

        level = "LOW"

    elif score < 60:

        level = "MEDIUM"

    else:

        level = "HIGH"

    return score, level