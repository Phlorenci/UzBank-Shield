from datetime import datetime, timezone
from unittest.mock import patch

from core.whois_checker import (
    _normalize_creation_date,
    _normalize_registrar,
    check_domain_info
)


def test_normalize_creation_date_from_datetime():

    aware_value = datetime(2015, 6, 1,tzinfo=timezone.utc)

    result = _normalize_creation_date(aware_value)

    assert result.tzinfo is None
    assert result == datetime(2015, 6, 1)

def test_normalize_creation_date_from_list():

    value = [datetime(2015, 6, 1), datetime(2016, 1, 1)]

    result = _normalize_creation_date(value)

    assert result == datetime(2015, 6, 1)


def test_normalize_creation_date_from_string():

    result = _normalize_creation_date("2015-06-01")

    assert result == datetime(2015, 6, 1)


def test_normalize_creation_date_invalid():

    result = _normalize_creation_date("not a date")

    assert result is None


def test_normalize_creation_date_empty_list():

    result = _normalize_creation_date([])

    assert result is None


def test_normalize_registrar_from_string():

    result = _normalize_registrar("  Example Registrar  ")

    assert result == "Example Registrar"


def test_normalize_registrar_from_list():

    result = _normalize_registrar(["Example Registrar", "Other"])

    assert result == "Example Registrar"


def test_normalize_registrar_none():

    result = _normalize_registrar(None)

    assert result is None


def test_check_domain_info_invalid_domain():
    # A domain that cannot resolve should fail gracefully
    # instead of raising an exception.

    result = check_domain_info(
        "this-domain-should-not-exist-uzbankshield.invalid"
    )

    assert result["available"] is False
    assert result["registrar"] is None
    assert result["created"] is None
    assert result["age_days"] is None
    assert result["error"] is not None

    def test_check_domain_info_invalid_domain():
        result = check_domain_info(
        "this-domain-should-not-exist-uzbankshield.invalid"
    )

    assert result["available"] is False
    assert result["registrar"] is None
    assert result["created"] is None
    assert result["age_days"] is None
    assert result["error"] is not None


def test_check_domain_info_success():
    fake_record = {
        "creation_date": datetime(2015, 6, 1),
        "registrar": "Example Registrar, LLC"
    }

    with patch(
        "core.whois_checker.whois.whois",
        return_value=fake_record
    ):
        result = check_domain_info("kapitalbank.uz")

    assert result["available"] is True
    assert result["registrar"] == "Example Registrar, LLC"
    assert result["created"] == "2015-06-01"
    assert result["age_days"] is not None
    assert result["error"] is None