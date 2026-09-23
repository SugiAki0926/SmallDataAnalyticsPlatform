# README

Small Data Analytics Platform は、データ分析基盤の仕組みを「小さく作って理解する」ための学習用プロジェクトです。

OpenWeather API からデータを取得し、PostgreSQL に保存。dlt で分析用DBへロードし、dbt で staging / intermediate / marts にモデリング。Airflow で一連のELTをオーケストレーションします。

Docker / Dev Containers で各コンポーネントを分離し、手元で確認しながら、壊しながら小さなデータ分析基盤を作成できます。

## データパイプラインとアーキテクチャ

実行する環境がRaspberryPiということもあり、1つのPostgreSQLで3つのデータベースを管理している。
また、Ingestionの部分は、日々、データが蓄積される基幹システムを模しているため、Airflowでは管理していない。

![Small Data Analytics Platform](sdap.png)

## コマンド

```
# 常駐コンテナ起動
docker compose -f compose.dev.yml up -d
docker build -t dap-source-ingestion:latest ./ingestion
docker build -t dap-dlt:latest ./extract_and_load
docker build -t dap-dbt:latest ./transform/dap_dbt

# Sourceへ1回インサート
docker run --rm --network dap-dev --env-file .env dap-source-ingestion:latest

# ELTを1回実行
docker exec dap-airflow-scheduler airflow dags unpause elt
docker exec dap-airflow-scheduler airflow dags trigger elt

# Martまでデータが届いているか
docker exec -it dap-postgres psql -U dap -d analytics -c "
SELECT city_name_en, current_weather_hour, temperature_celsius FROM dev_marts.mart_fct_current_weather
ORDER BY current_weather_hour DESC
LIMIT 5;
"
```
