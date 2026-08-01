from unittest.mock import patch, MagicMock

from core.page_analyzer import analyze_payment_page


def test_analyze_payment_page_detects_card_fields():
    html = """
    <form>
        <input name="card_number" type="text">
        <input name="cvv" type="text">
    </form>
    """

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = html

    with patch("core.page_analyzer.requests.get", return_value=mock_response):
        result = analyze_payment_page("https://example.com")

    assert result["analyzed"] is True
    assert result["requests_card_info"] is True
    assert len(result["matched_fields"]) > 0


def test_analyze_payment_page_no_card_fields():
    html = "<form><input name='email' type='text'></form>"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = html

    with patch("core.page_analyzer.requests.get", return_value=mock_response):
        result = analyze_payment_page("https://example.com")

    assert result["analyzed"] is True
    assert result["requests_card_info"] is False


def test_analyze_payment_page_handles_request_failure():
    import requests

    with patch("core.page_analyzer.requests.get", side_effect=requests.RequestException("timeout")):
        result = analyze_payment_page("https://example.com")

    assert result["analyzed"] is False
    assert result["requests_card_info"] is False
    assert result["error"] is not None


def test_analyze_payment_page_handles_error_status():
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("core.page_analyzer.requests.get", return_value=mock_response):
        result = analyze_payment_page("https://example.com")

    assert result["analyzed"] is False
    assert result["requests_card_info"] is False