from core.payment_verifier import load_payment_processors, verify_payment_processor


database = load_payment_processors()


def test_verified_payment_processor():
    result = verify_payment_processor("https://payme.uz", database)

    assert result["verified"] is True
    assert result["processor"] == "Payme"
    assert result["similarity"] == 100.0
    assert result["possible_typosquatting"] is False


def test_payment_processor_typosquatting():
    result = verify_payment_processor("https://paym3.uz", database)

    assert result["verified"] is False
    assert result["similarity"] >= 80
    assert result["possible_typosquatting"] is True


def test_unknown_domain_not_a_payment_processor():
    result = verify_payment_processor("https://google.com", database)

    assert result["verified"] is False
    assert result["processor"] is None
    assert result["closest_domain"] is None
    assert result["possible_typosquatting"] is False


def test_verified_click():
    result = verify_payment_processor("https://click.uz", database)

    assert result["verified"] is True
    assert result["processor"] == "Click"


def test_verified_uzcard():
    result = verify_payment_processor("https://uzcard.uz", database)

    assert result["verified"] is True
    assert result["processor"] == "Uzcard"


def test_verified_humo():
    result = verify_payment_processor("https://humocard.uz", database)

    assert result["verified"] is True
    assert result["processor"] == "Humo"