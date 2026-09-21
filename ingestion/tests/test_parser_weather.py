import parser_weather


def test_parse_geo(sample_geo):
    df = parser_weather.parse_geo(sample_geo)

    assert df.height == 1
    row = df.row(0, named=True)
    assert row["name"] == "Kyoto"
    assert row["local_name"] == "京都"
    assert row["country"] == "JP"


def test_parse_current_weather(sample_current_weather):
    df = parser_weather.parse_current_weather(sample_current_weather)

    assert df.height == 1
    row = df.row(0, named=True)
    assert row["dt"] == 1789808400
    assert row["weather_id"] == 800
    assert row["main"] == "Clear"
    assert row["temp"] == 299.79


def test_parse_forecast(sample_forecast):
    df = parser_weather.parse_forecast(sample_forecast)

    assert df.height == 1
    row = df.row(0, named=True)
    assert row["dt"] == 1789808400
    assert row["pod"] == "n"
    assert row["pop"] == 0.0


def test_parse_air_pollution(sample_air_pollution):
    df = parser_weather.parse_air_pollution(sample_air_pollution)

    assert df.height == 1
    row = df.row(0, named=True)
    assert row["aqi"] == 2
    assert row["pm2_5"] == 8.0


def test_with_city_id(sample_geo):
    df = parser_weather.with_city_id(parser_weather.parse_geo(sample_geo), "1857910")

    assert df["city_id"][0] == 1857910
