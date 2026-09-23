import os

import pendulum
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sdk import dag

JST = pendulum.timezone("Asia/Tokyo")
NETWORK = os.environ["DAP_DOCKER_NETWORK"]
DEPLOY_TARGET = os.environ["DBT_TARGET"]

_PG = {
    "POSTGRES_HOST": os.environ.get("POSTGRES_HOST", "postgres"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT", "5432"),
    "ANALYTICS_DB": os.environ["ANALYTICS_DB"],
    "TZ": os.environ.get("TZ", "Asia/Tokyo"),
}


# 失敗コンテナは auto_remove="success" で残る。
# 固定名だとリトライ時に衝突するため、実行時刻（マイクロ秒）で一意に設定。
_CONTAINER_NAME_SUFFIX = "{{ macros.datetime.utcnow().strftime('%Y%m%dT%H%M%S%f') }}"


def _docker(**kwargs) -> DockerOperator:
    return DockerOperator(
        network_mode=NETWORK,
        mount_tmp_dir=False,
        auto_remove="success",
        force_pull=False,
        **kwargs,
    )


@dag(
    dag_id="elt",
    start_date=pendulum.datetime(2026, 9, 21, tz=JST),
    schedule="5 * * * *",
    catchup=False,
    tags=["elt"],
)
def elt():
    extract_and_load = _docker(
        task_id="extract_and_load",
        image="dap-dlt:latest",
        command=["python", "main.py"],
        environment={
            **_PG,
            "SOURCE_DB": os.environ["SOURCE_DB"],
            "DLT_DB_USER": os.environ["DLT_DB_USER"],
            "DLT_DB_PASSWORD": os.environ["DLT_DB_PASSWORD"],
        },
        container_name=f"dap-dlt-run-{_CONTAINER_NAME_SUFFIX}",
    )
    dbt_build = _docker(
        task_id="dbt_build",
        image="dap-dbt:latest",
        command=["dbt", "build", "--target", DEPLOY_TARGET],
        environment={
            **_PG,
            "DBT_DB_USER": os.environ["DBT_DB_USER"],
            "DBT_DB_PASSWORD": os.environ["DBT_DB_PASSWORD"],
        },
        container_name=f"dap-dbt-run-{_CONTAINER_NAME_SUFFIX}",
    )

    extract_and_load >> dbt_build


elt()
