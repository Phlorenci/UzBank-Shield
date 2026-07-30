from unittest.mock import patch

from core.analyzer import URLAnalyzer
from core.database import load_official_domains


def test_analyze_returns_all_expected_keys():
    result = URLAnalyzer().analyze("https://kapitalbank.uz")

    expected_keys = {
        "components",
        "keywords",
        "verification",
        "payment_verification",
        "suspicious_tld",
        "connection",
        "ssl_info",
        "domain_info",
        "score",
        "level"
    }

    assert expected_keys.issubset(result.keys())


def test_analyze_verified_official_domain():
    result = URLAnalyzer().analyze("https://kapitalbank.uz")

    assert result["verification"]["verified"] is True
    assert result["verification"]["bank"] == "Kapitalbank"
    assert result["level"] in ("LOW", "MEDIUM", "HIGH")


def test_analyze_typosquatting_domain():
    result = URLAnalyzer().analyze("https://kapita1bank.uz")

    assert result["verification"]["verified"] is False
    assert result["verification"]["possible_typosquatting"] is True


def test_analyze_unknown_domain():
    result = URLAnalyzer().analyze("https://example.com")

    assert result["verification"]["verified"] is False
    assert result["verification"]["bank"] is None


def test_analyze_score_and_level_are_consistent():
    result = URLAnalyzer().analyze("https://kapitalbank.uz")

    score = result["score"]
    level = result["level"]

    assert 0 <= score <= 100

    if score < 30:
        assert level == "LOW"
    elif score < 60:
        assert level == "MEDIUM"
    else:
        assert level == "HIGH"


@patch("core.analyzer.check_domain_info")
@patch("core.analyzer.check_ssl_certificate")
@patch("core.analyzer.check_https")
def test_analyze_wiring_with_mocked_network_calls(
    mock_https,
    mock_ssl,
    mock_whois
):
    mock_https.return_value = {
        "protocol": "HTTPS",
        "https": True,
        "reachable": True,
        "status_code": 200
    }

    mock_ssl.return_value = {
        "valid": True,
        "issuer": "Test CA",
        "expires": "2027-01-01",
        "days_remaining": 300,
        "error": None
    }

    mock_whois.return_value = {
        "available": True,
        "registrar": "Test Registrar",
        "created": "2015-01-01",
        "age_days": 4000,
        "error": None
    }

    result = URLAnalyzer().analyze("https://kapitalbank.uz")

    assert result["connection"]["reachable"] is True
    assert result["ssl_info"]["valid"] is True
    assert result["domain_info"]["available"] is True

    # Fully verified, valid SSL, old domain, HTTPS -> should be low risk
    assert result["score"] < 30
    assert result["level"] == "LOW"