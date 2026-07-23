def calculate_risk_score(
    keywords,
    verification,
    suspicious_tld,
    connection,
    ssl_info
):
    score = 0

    # ---------------------------------
    # Phishing keywords
    # ---------------------------------

    score += len(keywords) * 15

    # ---------------------------------
    # Official bank verification
    # ---------------------------------

    if verification["verified"]:
        score -= 20

    # ---------------------------------
    # Bank impersonation
    # ---------------------------------

    if verification["possible_typosquatting"]:
        score += 35

    # ---------------------------------
    # Suspicious TLD
    # ---------------------------------

    if suspicious_tld:
        score += 20

    # ---------------------------------
    # HTTP connection
    # ---------------------------------

    if not connection["https"]:
        score += 15

    # ---------------------------------
    # Website unreachable
    # ---------------------------------

    if not connection["reachable"]:
        score += 10

    # ---------------------------------
    # SSL Certificate
    # ---------------------------------
    
    if ssl_info["valid"] is False:
        score += 25
    elif (
        ssl_info["valid"] is True
        and ssl_info["days_remaining"] is not None
        and ssl_info["days_remaining"] < 30
    ):
        score += 10
        
    # ---------------------------------
    # Clamp score
    # ---------------------------------

    score = max(0, min(score, 100))

    # ---------------------------------
    # Risk level
    # ---------------------------------

    if score < 30:
        level = "LOW"

    elif score < 60:
        level = "MEDIUM"

    else:
        level = "HIGH"

    return score, level