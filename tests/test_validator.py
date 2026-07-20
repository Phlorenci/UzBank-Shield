from core.validator import validate_url


def test_valid_https_url():
    assert validate_url("https://kapitalbank.uz") is True


def test_valid_http_url():
    assert validate_url("http://google.com") is True


def test_url_without_protocol():
    assert validate_url("kapitalbank.uz") is True


def test_invalid_url():
    assert validate_url("this is not a url") is False


def test_empty_url():
    assert validate_url("") is False