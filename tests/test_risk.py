from core.risk import calculate_risk_score

SAFE_SSL = {
    "valid": True,
    "days_remaining": 365
}

INVALID_SSL = {
    "valid": False,
    "days_remaining": None
}

EXPIRING_SSL = {
    "valid": True,
    "days_remaining": 10
}

SAFE_CONNECTION = {
    "https": True,
    "reachable": True
}

HTTP_CONNECTION = {
    "https": False,
    "reachable": True
}

UNREACHABLE_CONNECTION = {
    "https": True,
    "reachable": False
}

SAFE_DOMAIN_INFO = {
    "available": False,
    "registrar": None,
    "created": None,
    "age_days": None,
    "error": None
}

UNVERIFIED_PAYMENT = {
    "verified": False,
    "possible_typosquatting": False
}

VERIFIED_PAYMENT = {
    "verified": True,
    "possible_typosquatting": False
}

TYPOSQUAT_PAYMENT = {
    "verified": False,
    "possible_typosquatting": True
}


def test_verified_safe_domain():

    verification = {
        "verified": True,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        UNVERIFIED_PAYMENT,
        False,
        SAFE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
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
        UNVERIFIED_PAYMENT,
        False,
        SAFE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
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
        UNVERIFIED_PAYMENT,
        False,
        SAFE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
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
        UNVERIFIED_PAYMENT,
        True,
        SAFE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 20
    assert level == "LOW"


def test_http_connection():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        UNVERIFIED_PAYMENT,
        False,
        HTTP_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 15
    assert level == "LOW"


def test_unreachable_connection():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        UNVERIFIED_PAYMENT,
        False,
        UNREACHABLE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 10
    assert level == "LOW"


def test_invalid_ssl():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        UNVERIFIED_PAYMENT,
        False,
        SAFE_CONNECTION,
        INVALID_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 25
    assert level == "LOW"


def test_expiring_ssl():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        UNVERIFIED_PAYMENT,
        False,
        SAFE_CONNECTION,
        EXPIRING_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 10
    assert level == "LOW"


def test_verified_payment_processor():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        VERIFIED_PAYMENT,
        False,
        SAFE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 0
    assert level == "LOW"


def test_payment_processor_typosquatting():

    verification = {
        "verified": False,
        "possible_typosquatting": False
    }

    score, level = calculate_risk_score(
        [],
        verification,
        TYPOSQUAT_PAYMENT,
        False,
        SAFE_CONNECTION,
        SAFE_SSL,
        SAFE_DOMAIN_INFO
    )

    assert score == 35
    assert level == "MEDIUM"