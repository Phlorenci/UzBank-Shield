from core.risk import calculate_risk_score


verified = {
    "verified": True
}

unverified = {
    "verified": False
}


def test_low_risk():
    score, level = calculate_risk_score([], verified)

    assert level == "LOW"


def test_medium_risk():
    score, level = calculate_risk_score(
        ["login"],
        unverified
    )

    assert level == "MEDIUM"


def test_high_risk():
    score, level = calculate_risk_score(
        ["login", "verify", "bank"],
        unverified
    )

    assert level == "HIGH"


def test_verified_score_lower():
    verified_score, _ = calculate_risk_score(
        ["login"],
        verified
    )

    unverified_score, _ = calculate_risk_score(
        ["login"],
        unverified
    )

    assert verified_score < unverified_score