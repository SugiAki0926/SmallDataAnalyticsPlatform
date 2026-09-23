#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

git checkout main
git pull --ff-only origin main

docker build -t dap-source-ingestion:latest ingestion
docker build -t dap-dlt:latest extract_and_load
docker build -t dap-dbt:latest transform/dap_dbt
docker build -t dap-airflow:latest airflow

docker compose -f compose.prod.yml up -d

echo "deployed $(git rev-parse HEAD)"
