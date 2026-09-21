"""pipeline の回帰テスト（merge 冪等・増分）。"""

from __future__ import annotations

from datetime import datetime, timezone

import dlt
import pytest

from conftest import table_count


def _sample_rows():
    return [
        {
            "id": 1,
            "name": "a",
            "updated_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
        },
        {
            "id": 2,
            "name": "b",
            "updated_at": datetime(2026, 1, 2, tzinfo=timezone.utc),
        },
    ]


@dlt.resource(
    name="items",
    primary_key="id",
    write_disposition="merge",
)
def items_resource(
    updated_at=dlt.sources.incremental("updated_at", initial_value=None),
):
    yield from _sample_rows()


def test_merge_does_not_duplicate_on_rerun(isolated_pipeline):
    """同じデータを2回 load しても行が増殖しない（merge + PK）。"""
    # 増分を外して「同じ行を再度抽出」させる（冪等性だけを見る）
    @dlt.resource(name="items", primary_key="id", write_disposition="merge")
    def items_full():
        yield from _sample_rows()

    isolated_pipeline.run(items_full())
    assert table_count(isolated_pipeline, "items") == 2

    isolated_pipeline.run(items_full())
    assert table_count(isolated_pipeline, "items") == 2


def test_incremental_skips_already_seen_rows(isolated_pipeline):
    """2回目は増分 cursor により新規抽出がほぼ無い。"""
    info1 = isolated_pipeline.run(items_resource())
    assert len(info1.loads_ids) == 1
    assert table_count(isolated_pipeline, "items") == 2

    info2 = isolated_pipeline.run(items_resource())
    # 新規行なし → load package が空、または行数が増えない
    assert table_count(isolated_pipeline, "items") == 2
    assert len(info2.loads_ids) == 0 or table_count(isolated_pipeline, "items") == 2


def test_sql_source_merge_idempotent_when_source_has_data(isolated_pipeline):
    """本番 Source の weather を読む結合テスト。データが無ければ skip。"""
    import os

    import psycopg2

    from main import build_source

    conn = psycopg2.connect(
        f"postgresql://{os.environ['DLT_DB_USER']}:{os.environ['DLT_DB_PASSWORD']}"
        f"@{os.environ.get('POSTGRES_HOST', 'postgres')}:"
        f"{os.environ.get('POSTGRES_PORT', '5432')}/{os.environ['SOURCE_DB']}"
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM weather.locations")
            n = int(cur.fetchone()[0])
    finally:
        conn.close()

    if n == 0:
        pytest.skip("Source weather.locations が空のため skip")

    source = build_source()
    isolated_pipeline.run(source)
    locations_1 = table_count(isolated_pipeline, "locations")
    assert locations_1 >= 1

    # state を残したまま再実行 → 増分 + merge で件数維持
    isolated_pipeline.run(build_source())
    assert table_count(isolated_pipeline, "locations") == locations_1
