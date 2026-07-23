from core.database import load_official_domains
from core.similarity import (
    calculate_similarity,
    find_closest_domain
)

database = load_official_domains()


def test_similarity_score():
    similarity = calculate_similarity(
        "kapitalbank.uz",
        "kapita1bank.uz"
    )

    assert similarity > 80


def test_find_closest_domain():
    result = find_closest_domain(
        "https://kapita1bank.uz",
        database
    )

    assert result["bank"] == "Kapitalbank"
    assert result["similarity"] > 80