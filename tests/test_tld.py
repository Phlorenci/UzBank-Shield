from core.tld import (
    get_tld,
    is_suspicious_tld
)


def test_get_tld():

    assert get_tld("https://kapitalbank.uz") == ".uz"
    assert get_tld("https://google.com") == ".com"


def test_safe_tld():

    assert is_suspicious_tld(
        "https://kapitalbank.uz"
    ) is False


def test_suspicious_tld():

    assert is_suspicious_tld(
        "https://kapitalbank.xyz"
    ) is True