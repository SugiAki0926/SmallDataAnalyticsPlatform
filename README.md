# README

Small Data Analytics Platform は、データ分析基盤の仕組みを「小さく作って理解する」ための学習用プロジェクトです。

OpenWeather API からデータを取得し、PostgreSQL に保存。dlt で分析用DBへロードし、dbt で staging / intermediate / marts にモデリング。Airflow で一連のELTをオーケストレーションします。

Docker / Dev Containers で各コンポーネントを分離し、手元で確認しながら、壊しながら小さなデータ分析基盤を作成できます。

## データパイプラインとアーキテクチャ

実行する環境がRaspberryPiということもあり、1つのPostgreSQLで3つのデータベースを管理しています。
また、Ingestionの部分は、日々、データが蓄積される基幹システムを模しているため、Airflowでは管理していません。

![Small Data Analytics Platform](sdap.png)

本プロジェクトは、データ分析基盤の仕組みを「小さく作って理解する」ことを目的とした学習用です。そのため、セキュリティや監視、詳細なログなど本番運用で必須となる機能は、簡易的な実装のみです。

## 本番運用

### 起動と停止

基本的には、起動は **main への merge → GitHub Actions の runner → `deploy.sh`** です。
Githubリポジトリへのシークレットの登録が必要です。ただ、手元のローカルPCで開発するには必須ではありません。
変更は PR を merge し、次の deploy で反映します。

```bash
cd /opt/SmallDataAnalyticsPlatform
docker compose -f compose.prod.yml up -d
docker compose -f compose.prod.yml stop

# log
docker logs dap-prod-airflow-scheduler
docker logs dap-prod-postgres
cat /home/raspy/source-ingestion.log
```

各コンテナが正常に起動した後は、初回￥cronへの



OpenWeather から Source DB への取り込みは、`raspy` の crontab です。毎時 0 分（JST）に実行し、ELT の DAG は毎時 5 分です。
```bash
crontab -l
```
