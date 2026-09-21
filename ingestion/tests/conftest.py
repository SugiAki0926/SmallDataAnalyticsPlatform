import pytest


@pytest.fixture
def sample_geo() -> list[dict]:
    return [
        {
            "name": "Kyoto",
            "local_names": {"ja": "京都"},
            "lat": 35.0116,
            "lon": 135.7681,
            "country": "JP",
        }
    ]


@pytest.fixture
def sample_current_weather() -> dict:
    return {
        "dt": 1789808400,
        "weather": [
            {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
        ],
        "main": {
            "temp": 299.79,
            "feels_like": 299.79,
            "temp_min": 299.79,
            "temp_max": 300.5,
            "pressure": 1013,
            "humidity": 60,
            "sea_level": 1013,
            "grnd_level": 1010,
        },
        "visibility": 10000,
        "wind": {"speed": 2.5, "deg": 180, "gust": 4.0},
        "clouds": {"all": 10},
        "sys": {"sunrise": 1789780000, "sunset": 1789825000},
        "timezone": 32400,
    }


@pytest.fixture
def sample_forecast() -> dict:
    return {
        "list": [
            {
                "dt": 1789808400,
                "main": {
                    "temp": 299.79,
                    "feels_like": 299.79,
                    "temp_min": 299.79,
                    "temp_max": 300.5,
                    "pressure": 1013,
                    "sea_level": 1013,
                    "grnd_level": 1010,
                    "humidity": 60,
                },
                "weather": [
                    {
                        "id": 800,
                        "main": "Clear",
                        "description": "clear sky",
                        "icon": "01n",
                    }
                ],
                "clouds": {"all": 0},
                "wind": {"speed": 2.0, "deg": 90, "gust": 3.0},
                "visibility": 10000,
                "pop": 0.0,
                "sys": {"pod": "n"},
            }
        ]
    }


@pytest.fixture
def sample_air_pollution() -> dict:
    return {
        "list": [
            {
                "dt": 1789808400,
                "main": {"aqi": 2},
                "components": {
                    "co": 200.0,
                    "no": 0.1,
                    "no2": 10.0,
                    "o3": 50.0,
                    "so2": 1.0,
                    "pm2_5": 8.0,
                    "pm10": 12.0,
                    "nh3": 0.5,
                },
            }
        ]
    }
