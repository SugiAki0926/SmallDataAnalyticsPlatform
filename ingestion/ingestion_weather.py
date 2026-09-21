import os
import polars as pl
import psycopg

def connect():
    return psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "postgres"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
        dbname=os.environ["SOURCE_DB"],
        user=os.environ["SOURCE_DB_USER"],
        password=os.environ["SOURCE_DB_PASSWORD"],
    )


def _row(df: pl.DataFrame, index: int = 0) -> dict:
    return df.row(index, named=True)

def upsert_location(cur, geo_df: pl.DataFrame) -> None:
    row = _row(geo_df)
    cur.execute(
        """
        INSERT INTO weather.locations (
            city_id, name, local_name, country, lat, lon
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (city_id) DO UPDATE SET
            name = EXCLUDED.name,
            local_name = EXCLUDED.local_name,
            country = EXCLUDED.country,
            lat = EXCLUDED.lat,
            lon = EXCLUDED.lon,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            int(row["city_id"]),
            row["name"],
            row.get("local_name"),
            row["country"],
            float(row["lat"]),
            float(row["lon"]),
        ),
    )


def upsert_current_weather(cur, weather_df: pl.DataFrame):
    row = _row(weather_df)
    cur.execute(
        """
        INSERT INTO weather.current_weather (
            city_id, dt,
            weather_id, main, description, icon,
            temp, feels_like, temp_min, temp_max,
            pressure, humidity, sea_level, grnd_level,
            visibility, speed, deg, gust, clouds_all,
            sunrise, sunset, timezone
        ) VALUES (
            %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )
        ON CONFLICT (city_id, dt) DO UPDATE SET
            weather_id = EXCLUDED.weather_id,
            main = EXCLUDED.main,
            description = EXCLUDED.description,
            icon = EXCLUDED.icon,
            temp = EXCLUDED.temp,
            feels_like = EXCLUDED.feels_like,
            temp_min = EXCLUDED.temp_min,
            temp_max = EXCLUDED.temp_max,
            pressure = EXCLUDED.pressure,
            humidity = EXCLUDED.humidity,
            sea_level = EXCLUDED.sea_level,
            grnd_level = EXCLUDED.grnd_level,
            visibility = EXCLUDED.visibility,
            speed = EXCLUDED.speed,
            deg = EXCLUDED.deg,
            gust = EXCLUDED.gust,
            clouds_all = EXCLUDED.clouds_all,
            sunrise = EXCLUDED.sunrise,
            sunset = EXCLUDED.sunset,
            timezone = EXCLUDED.timezone,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            int(row["city_id"]),
            row["dt"],
            row["weather_id"],
            row["main"],
            row["description"],
            row["icon"],
            row["temp"],
            row["feels_like"],
            row["temp_min"],
            row["temp_max"],
            row["pressure"],
            row["humidity"],
            row["sea_level"],
            row["grnd_level"],
            row["visibility"],
            row["speed"],
            row["deg"],
            row.get("gust"),
            row["clouds_all"],
            row["sunrise"],
            row["sunset"],
            row["timezone"],
        ),
    )


# forecastsは意図的にupsertしない。
def insert_forecasts(cur, forecast_df: pl.DataFrame):
    for row in forecast_df.iter_rows(named=True):
        cur.execute(
            """
            INSERT INTO weather.weather_forecasts (
                city_id, dt,
                temp, feels_like, temp_min, temp_max,
                pressure, sea_level, grnd_level, humidity,
                weather_id, main, description, icon,
                clouds_all, speed, deg, gust,
                visibility, pop, pod
            ) VALUES (
                %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s
            )
            """,
            (
                int(row["city_id"]),
                row["dt"],
                row["temp"],
                row["feels_like"],
                row["temp_min"],
                row["temp_max"],
                row["pressure"],
                row["sea_level"],
                row["grnd_level"],
                row["humidity"],
                row["weather_id"],
                row["main"],
                row["description"],
                row["icon"],
                row["clouds_all"],
                row["speed"],
                row["deg"],
                row.get("gust"),
                row["visibility"],
                row.get("pop"),
                row.get("pod"),
            ),
        )


def upsert_air_pollution(cur, air_pollution_df: pl.DataFrame):
    for row in air_pollution_df.iter_rows(named=True):
        cur.execute(
            """
            INSERT INTO weather.air_pollution (
                city_id, dt, aqi,
                co, "no", no2, o3, so2, pm2_5, pm10, nh3
            ) VALUES (
                %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (city_id, dt) DO UPDATE SET
                aqi = EXCLUDED.aqi,
                co = EXCLUDED.co,
                "no" = EXCLUDED."no",
                no2 = EXCLUDED.no2,
                o3 = EXCLUDED.o3,
                so2 = EXCLUDED.so2,
                pm2_5 = EXCLUDED.pm2_5,
                pm10 = EXCLUDED.pm10,
                nh3 = EXCLUDED.nh3,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                int(row["city_id"]),
                row["dt"],
                row["aqi"],
                row["co"],
                row["no"],
                row["no2"],
                row["o3"],
                row["so2"],
                row["pm2_5"],
                row["pm10"],
                row["nh3"],
            ),
        )


def ingest(
    geo_df: pl.DataFrame,
    weather_df: pl.DataFrame,
    forecast_df: pl.DataFrame,
    air_pollution_df: pl.DataFrame,
) -> None:
    with connect() as conn:
        with conn.cursor() as cur:
            upsert_location(cur, geo_df)
            upsert_current_weather(cur, weather_df)
            insert_forecasts(cur, forecast_df)
            upsert_air_pollution(cur, air_pollution_df)
        conn.commit()
