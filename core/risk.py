def calculate_risk_score(keywords):
    score = len(keywords) * 15

    if score > 100:
        score = 100

    if score < 30:
        level = "LOW"

    elif score < 60:
        level = "MEDIUM"

    else:
        level = "HIGH"

    return score, level