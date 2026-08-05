from unittest.mock import patch, MagicMock

import pytest

from core.ai_assistant import ask_assistant, AssistantError, _format_scan_context


def test_ask_assistant_raises_without_api_key():
    with pytest.raises(AssistantError, match="No OpenAI API key"):
        ask_assistant("", "What is typosquatting?")


def test_format_scan_context_returns_none_without_result():
    assert _format_scan_context(None) is None


def test_format_scan_context_includes_key_fields():
    scan_result = {
        "components": {"original_url": "https://kapita1bank.uz"},
        "score": 65,
        "level": "HIGH",
        "verification": {
            "verified": False,
            "bank": None,
            "possible_typosquatting": True,
            "closest_domain": "kapitalbank.uz",
            "similarity": 95.0
        },
        "payment_verification": {
            "verified": False,
            "processor": None
        },
        "connection": {"https": True},
        "suspicious_tld": False,
        "page_analysis": {"requests_card_info": False}
    }

    context = _format_scan_context(scan_result)

    assert "kapita1bank.uz" in context
    assert "65/100" in context
    assert "HIGH" in context
    assert "kapitalbank.uz" in context
    assert "95.0%" in context


@patch("core.ai_assistant.OpenAI")
def test_ask_assistant_success(mock_openai_class):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This looks like a typosquat."
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_class.return_value = mock_client

    result = ask_assistant("sk-fake-key", "Why is this suspicious?")

    assert result == "This looks like a typosquat."
    mock_client.chat.completions.create.assert_called_once()


@patch("core.ai_assistant.OpenAI")
def test_ask_assistant_wraps_authentication_error(mock_openai_class):
    from openai import AuthenticationError

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = AuthenticationError(
        message="Invalid key", response=MagicMock(status_code=401), body=None
    )
    mock_openai_class.return_value = mock_client

    with pytest.raises(AssistantError, match="Invalid OpenAI API key"):
        ask_assistant("sk-bad-key", "test question")