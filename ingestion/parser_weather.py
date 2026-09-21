import polars as pl


def with_city_id(df: pl.DataFrame, city_id: str) -> pl.DataFrame:
    return df.with_columns(pl.lit(int(city_id)).alias("city_id"))


def parse_geo(geo: list[dict]) -> pl.DataFrame:
    parsed_df = pl.DataFrame(geo).select(
        pl.col("name"),
        pl.col("local_names").struct.field("ja").alias("local_name"),
        pl.col("lat"),
        pl.col("lon"),
        pl.col("country"),
    )

    return parsed_df

def parse_current_weather(current_weather: dict) -> pl.DataFrame:
    parsed_df = pl.DataFrame([current_weather]).select(
        pl.col("dt"),
        pl.col("weather").list.first().struct.field("id").alias("weather_id"),
        pl.col("weather").list.first().struct.field("main"),
        pl.col("weather").list.first().struct.field("description"),
        pl.col("weather").list.first().struct.field("icon"),
        pl.col("main").struct.field("temp"),
        pl.col("main").struct.field("feels_like"),
        pl.col("main").struct.field("temp_min"),
        pl.col("main").struct.field("temp_max"),
        pl.col("main").struct.field("pressure"),
        pl.col("main").struct.field("humidity"),
        pl.col("main").struct.field("sea_level"),
        pl.col("main").struct.field("grnd_level"),
        pl.col("visibility"),
        pl.col("wind").struct.field("speed"),
        pl.col("wind").struct.field("deg"),
        pl.col("wind").struct.field("gust"),
        pl.col("clouds").struct.field("all").alias("clouds_all"),
        pl.col("sys").struct.field("sunrise"),
        pl.col("sys").struct.field("sunset"),
        pl.col("timezone"),
    )

    return parsed_df


def parse_forecast(forecast: dict) -> pl.DataFrame:
    tmp_df = pl.DataFrame(forecast["list"])
    parsed_df = tmp_df.select(
        pl.col("dt"),
        pl.col("main").struct.field("temp"),
        pl.col("main").struct.field("feels_like"),
        pl.col("main").struct.field("temp_min"),
        pl.col("main").struct.field("temp_max"),
        pl.col("main").struct.field("pressure"),
        pl.col("main").struct.field("sea_level"),
        pl.col("main").struct.field("grnd_level"),
        pl.col("main").struct.field("humidity"),
        pl.col("weather").list.first().struct.field("id").alias("weather_id"),
        pl.col("weather").list.first().struct.field("main"),
        pl.col("weather").list.first().struct.field("description"),
        pl.col("weather").list.first().struct.field("icon"),
        pl.col("clouds").struct.field("all").alias("clouds_all"),
        pl.col("wind").struct.field("speed"),
        pl.col("wind").struct.field("deg"),
        pl.col("wind").struct.field("gust"),
        pl.col("visibility"),
        pl.col("pop"),
        pl.col("sys").struct.field("pod"),
    )

    return parsed_df


def parse_air_pollution(air_pollution: dict) -> pl.DataFrame:
    return pl.DataFrame(air_pollution["list"]).select(
        pl.col("dt"),
        pl.col("main").struct.field("aqi"),
        pl.col("components").struct.field("co"),
        pl.col("components").struct.field("no"),
        pl.col("components").struct.field("no2"),
        pl.col("components").struct.field("o3"),
        pl.col("components").struct.field("so2"),
        pl.col("components").struct.field("pm2_5"),
        pl.col("components").struct.field("pm10"),
        pl.col("components").struct.field("nh3"),
    )
