def calculate_risk_score(
    keywords,
    verification,
    payment_verification,
    page_analysis,  
    suspicious_tld,
    connection,
    ssl_info,
    domain_info,
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
    # Domain age
    # ---------------------------------

    if domain_info["available"] and domain_info["age_days"] is not None:

        if domain_info["age_days"] < 30:
            score += 25

        elif domain_info["age_days"] < 180:
            score += 10

    # ---------------------------------
    # Official payment processor verification
    # ---------------------------------

    if payment_verification["verified"]:
        score -= 20

    # ---------------------------------
    # Payment processor impersonation
    # ---------------------------------

    if payment_verification["possible_typosquatting"]:
        score += 35

    # ---------------------------------
    # Payment page requesting card info on unverified domain
    # ---------------------------------

    is_verified_anywhere = verification["verified"] or payment_verification["verified"]

    if page_analysis["requests_card_info"] and not is_verified_anywhere:
        score += 40
        
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