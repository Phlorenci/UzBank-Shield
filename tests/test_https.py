from core.https_checker import check_https


def test_https():

    result = check_https(
        "https://kapitalbank.uz"
    )

    assert result["https"] is True


def test_http():

    result = check_https(
        "http://example.com"
    )

    assert result["https"] is False