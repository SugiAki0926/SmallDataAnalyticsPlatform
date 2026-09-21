import json
import urllib.error
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

import fetch_weather


def test_require_env_missing(monkeypatch):
    monkeypatch.delenv("MISSING_TEST_ENV_VAR", raising=False)

    with pytest.raises(SystemExit) as exc_info:
        fetch_weather._require_env("MISSING_TEST_ENV_VAR")

    assert exc_info.value.code == 1


@patch("urllib.request.urlopen")
def test_fetch_geo_returns_json(mock_urlopen):
    payload = [{"name": "Kyoto", "lat": 35.0, "lon": 135.0, "country": "JP"}]
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(payload).encode()
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)
    mock_urlopen.return_value = mock_response

    result = fetch_weather.fetch_geo("test-key", "Kyoto")

    assert result == payload
    mock_urlopen.assert_called_once()


@patch("urllib.request.urlopen")
def test_get_json_http_error_exits(mock_urlopen):
    body = b'{"cod":401,"message":"Invalid API key"}'
    error = urllib.error.HTTPError(
        url="https://example.com",
        code=401,
        msg="Unauthorized",
        hdrs=None,
        fp=BytesIO(body),
    )
    mock_urlopen.side_effect = error

    with pytest.raises(SystemExit) as exc_info:
        fetch_weather.fetch_geo("bad-key", "Kyoto")

    assert exc_info.value.code == 1
