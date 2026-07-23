from core.risk import calculate_risk_score


def test_verified_safe_domain():

    verification = {
        "verified": True,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        False
    )

    assert score == 0
    assert level == "LOW"


def test_keyword_risk():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        ["login", "verify"],
        verification,
        False
    )

    assert score == 30
    assert level == "MEDIUM"


def test_typosquatting():

    verification = {
        "verified": False,
        "possible_typosquatting": True
    }

    score, level = calculate_risk_score(
        [],
        verification,
        False
    )

    assert score == 35
    assert level == "MEDIUM"


def test_suspicious_tld():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        True
    )

    assert score == 20
    assert level == "LOW"