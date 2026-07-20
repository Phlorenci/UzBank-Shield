from core.parser import extract_url_components


def test_extract_full_url():
    components = extract_url_components(
        "https://kapitalbank.uz/login?id=123#home"
    )

    assert components["protocol"] == "https"
    assert components["domain"] == "kapitalbank.uz"
    assert components["path"] == "/login"
    assert components["query"] == "id=123"
    assert components["fragment"] == "home"


def test_url_without_protocol():
    components = extract_url_components("kapitalbank.uz")

    assert components["protocol"] == "https"
    assert components["domain"] == "kapitalbank.uz"


def test_empty_path():
    components = extract_url_components("https://google.com")

    assert components["path"] == ""