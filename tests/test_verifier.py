from core.verifier import verify_domain
from core.database import load_official_domains


database = load_official_domains()


def test_verified_bank():
    result = verify_domain(
        "https://kapitalbank.uz",
        database
    )

    assert result["verified"] is True
    assert result["bank"] == "Kapitalbank"


def test_unknown_domain():
    result = verify_domain(
        "https://google.com",
        database
    )

    assert result["verified"] is False


def test_subdomain():
    result = verify_domain(
        "https://www.kapitalbank.uz",
        database
    )

    assert result["verified"] is True