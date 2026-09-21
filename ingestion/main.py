import sys

import fetch_weather
import ingestion_weather
import parser_weather


def run() -> None:
    api_key = fetch_weather._require_env("OPENWEATHER_API_KEY")
    base_url = fetch_weather._require_env("OPENWEATHER_BASE_URL")
    city_id = fetch_weather._require_env("OPENWEATHER_CITY_ID")
    city_query = fetch_weather._require_env("OPENWEATHER_CITY_QUERY")
    forecast_cnt = int(fetch_weather.os.environ.get("OPENWEATHER_FORECAST_CNT", "8"))

    # Locations
    geo = fetch_weather.fetch_geo(api_key, city_query)
    geo_df = parser_weather.with_city_id(parser_weather.parse_geo(geo), city_id)

    # Current weather
    current_weather = fetch_weather.fetch_current_weather(base_url, api_key, city_id)
    weather_df = parser_weather.with_city_id(parser_weather.parse_current_weather(current_weather), city_id)

    # Forecast
    forecast = fetch_weather.fetch_forecast(base_url, api_key, city_id, forecast_cnt)
    forecast_df = parser_weather.with_city_id(parser_weather.parse_forecast(forecast), city_id)

    # Air pollution
    air_pollution = fetch_weather.fetch_air_pollution(base_url, api_key, city_query, geo=geo)
    air_pollution_df = parser_weather.with_city_id(parser_weather.parse_air_pollution(air_pollution), city_id)

    # Ingest to SourceDB
    ingestion_weather.ingest(
        geo_df=geo_df,
        weather_df=weather_df,
        forecast_df=forecast_df,
        air_pollution_df=air_pollution_df,
    )
    print("Inserted successfully")


if __name__ == "__main__":
    try:
        run()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        sys.exit(code)
    except Exception as exc:
        print(f"ingestion failed: {exc}", file=sys.stderr)
        sys.exit(1)
