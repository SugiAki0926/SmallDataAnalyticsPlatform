"""extract_and_load の pytest 用フィクスチャ。

隔離方針:
- 本番 dataset `raw` / pipeline `source_to_analytics` は触らない
- Analytics 上に専用 dataset（schema）を作り、テスト後に DROP
- ローカル dlt working dir は tmp_path（テスト間で state を共有しない）
"""

from __future__ import annotations

import os

import pytest

from main import _pg_url, build_pipeline

TEST_PIPELINE_NAME = "source_to_analytics_pytest"
TEST_DATASET_NAME = "raw_pytest"


@pytest.fixture
def isolated_pipeline(tmp_path):
    """本番 raw と分離した pipeline + 終了時に dataset を破棄する。"""
    pipeline = build_pipeline(
        pipeline_name=TEST_PIPELINE_NAME,
        dataset_name=TEST_DATASET_NAME,
        pipelines_dir=str(tmp_path / "pipelines"),
    )
    yield pipeline
    _drop_dataset(TEST_DATASET_NAME)
    _drop_dataset(f"{TEST_DATASET_NAME}_staging")


def _drop_dataset(dataset_name: str) -> None:
    """worker_dlt が所有するテスト用 schema を落とす。"""
    import psycopg2

    conn = psycopg2.connect(_pg_url(os.environ["ANALYTICS_DB"]))
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(f'DROP SCHEMA IF EXISTS "{dataset_name}" CASCADE')
    finally:
        conn.close()


def table_count(pipeline, table_name: str) -> int:
    with pipeline.sql_client() as client:
        qualified = client.make_qualified_table_name(table_name)
        with client.execute_query(f"SELECT COUNT(*) FROM {qualified}") as cur:
            row = cur.fetchone()
            return int(row[0])
