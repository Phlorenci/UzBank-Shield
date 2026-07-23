from core.database import load_official_domains
from core.verifier import verify_domain

database = load_official_domains()


def test_verified_domain():

    result = verify_domain(
        "https://kapitalbank.uz",
        database
    )

    assert result["verified"] is True
    assert result["similarity"] == 100.0
    assert result["possible_typosquatting"] is False


def test_similar_fake_domain():

    result = verify_domain(
        "https://kapita1bank.uz",
        database
    )

    assert result["verified"] is False
    assert result["similarity"] >= 80
    assert result["possible_typosquatting"] is True


def test_unknown_domain():

    result = verify_domain(
        "https://google.com",
        database
    )

    assert result["verified"] is False
    assert result["bank"] is None
    assert result["closest_domain"] is None
    assert result["possible_typosquatting"] is False