import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GEO_BASE_URL = "https://api.openweathermap.org/geo/1.0"


def _fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        _fail(f"{name} is not set. Please set it in the environment variables.")
    return value


def _get_json(url: str):
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        endpoint = url.split("?", 1)[0]
        _fail(f"HTTP {exc.code} {exc.reason}: {endpoint}: {body}")
    except urllib.error.URLError as exc:
        _fail(f"Connection failed: {exc.reason}")


def _url(base: str, path: str, params: dict) -> str:
    return f"{base.rstrip('/')}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"


def fetch_current_weather(base_url: str, api_key: str, city_id: str) -> dict:
    return _get_json(_url(base_url, "weather", {"id": city_id, "appid": api_key}))


def fetch_forecast(base_url: str, api_key: str, city_id: str, cnt: int = 8) -> dict:
    return _get_json(_url(base_url, "forecast", {"id": city_id, "cnt": cnt, "appid": api_key}))


# Air Pollution API は city id 非対応。lat/lon が必須。
def fetch_air_pollution(base_url: str, api_key: str, city_query: str, geo: list) -> dict:
    if geo is None:
        if not city_query:
            _fail("city_query is required when geo is not provided")
        geo = fetch_geo(api_key, city_query)
    return _get_json(_url(base_url, "air_pollution", {"lat": geo[0]["lat"], "lon": geo[0]["lon"], "appid": api_key}))


def fetch_geo(api_key: str, city_query: str) -> list:
    return _get_json(_url(GEO_BASE_URL, "direct", {"q": city_query, "limit": 1, "appid": api_key}))
