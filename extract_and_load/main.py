import os
import sys

import dlt
from dlt.sources.sql_database import sql_database

# extractする対象テーブル
TABLES = (
    "locations",
    "current_weather",
    "weather_forecasts",
    "air_pollution",
)

PRIMARY_KEYS = {
    "locations": "city_id",
    "current_weather": "current_weather_id",
    "weather_forecasts": "weather_forecast_id",
    "air_pollution": "air_pollution_id",
}


def _pg_url(dbname: str) -> str:
    user = os.environ["DLT_DB_USER"]
    password = os.environ["DLT_DB_PASSWORD"]
    host = os.environ.get("POSTGRES_HOST", "postgres")
    port = os.environ.get("POSTGRES_PORT", "5432")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def build_source():
    source = sql_database(
        credentials=_pg_url(os.environ["SOURCE_DB"]),
        schema="weather",
    ).with_resources(*TABLES)

    for name in TABLES:
        getattr(source, name).apply_hints(
            primary_key=PRIMARY_KEYS[name],
            write_disposition="merge",
            incremental=dlt.sources.incremental("updated_at"),
        )
    return source


def build_pipeline(
    *,
    pipeline_name: str,
    dataset_name: str,
    pipelines_dir: str | None = None,
):
    # pipeline_name + destination + dataset_name が state の識別キー。
    # ローカル /var/dlt/.../state.json は Container と消えても、
    # Analytics raw._dlt_pipeline_state から restore される（dlt デフォルト）。
    kwargs = {
        "pipeline_name": pipeline_name,
        "destination": dlt.destinations.postgres(
            credentials=_pg_url(os.environ["ANALYTICS_DB"]),
        ),
        "dataset_name": dataset_name,
    }
    if pipelines_dir is not None:
        kwargs["pipelines_dir"] = pipelines_dir
    return dlt.pipeline(**kwargs)


def run():
    pipeline = build_pipeline(pipeline_name="source_to_analytics", dataset_name="raw")
    load_info = pipeline.run(build_source())
    print(load_info)
    return load_info


if __name__ == "__main__":
    try:
        run()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        sys.exit(code)
    except Exception as exc:
        print(f"extract_and_load failed: {exc}", file=sys.stderr)

        sys.exit(1)
