from core.messages import get_message


def test_get_message_english():
    assert get_message("invalid_url", "en") == "Invalid URL format."


def test_get_message_russian():
    result = get_message("invalid_url", "ru")
    assert result == "Неверный формат URL."


def test_get_message_uzbek():
    result = get_message("invalid_url", "uz")
    assert result == "URL formati noto'g'ri."


def test_get_message_unsupported_language_falls_back_to_english():
    result = get_message("invalid_url", "fr")
    assert result == "Invalid URL format."


def test_get_message_unknown_key_returns_key_itself():
    result = get_message("nonexistent_key", "en")
    assert result == "nonexistent_key"