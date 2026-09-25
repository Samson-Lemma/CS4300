from unittest.mock import Mock, patch

from src.task7 import get_json


@patch("src.task7.requests.get")
def test_get_json(mock_get):
    fake_response = Mock()

    fake_response.json.return_value = {
        "id": 1,
        "title": "Test item",
    }

    mock_get.return_value = fake_response

    result = get_json("https://example.com/api")

    assert result == {
        "id": 1,
        "title": "Test item",
    }

    mock_get.assert_called_once_with(
        "https://example.com/api",
        timeout=5,
    )

    fake_response.raise_for_status.assert_called_once()