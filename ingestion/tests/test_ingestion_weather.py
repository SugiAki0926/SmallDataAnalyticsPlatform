from unittest.mock import MagicMock

import ingestion_weather
import parser_weather


def test_ingest_commits_all_writes(
    monkeypatch,
    sample_geo,
    sample_current_weather,
    sample_forecast,
    sample_air_pollution,
):
    city_id = "1857910"
    geo_df = parser_weather.with_city_id(parser_weather.parse_geo(sample_geo), city_id)
    weather_df = parser_weather.with_city_id(
        parser_weather.parse_current_weather(sample_current_weather), city_id
    )
    forecast_df = parser_weather.with_city_id(
        parser_weather.parse_forecast(sample_forecast), city_id
    )
    air_pollution_df = parser_weather.with_city_id(
        parser_weather.parse_air_pollution(sample_air_pollution), city_id
    )

    mock_cur = MagicMock()
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    monkeypatch.setattr(ingestion_weather, "connect", lambda: mock_conn)

    ingestion_weather.ingest(
        geo_df=geo_df,
        weather_df=weather_df,
        forecast_df=forecast_df,
        air_pollution_df=air_pollution_df,
    )

    assert mock_cur.execute.call_count == 4
    sql_calls = [call.args[0] for call in mock_cur.execute.call_args_list]
    assert any("weather.locations" in sql for sql in sql_calls)
    assert any("weather.current_weather" in sql for sql in sql_calls)
    assert any("weather.weather_forecasts" in sql for sql in sql_calls)
    assert any("weather.air_pollution" in sql for sql in sql_calls)
    mock_conn.commit.assert_called_once()
