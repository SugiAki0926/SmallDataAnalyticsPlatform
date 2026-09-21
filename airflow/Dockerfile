FROM python:3.12-slim-bookworm

ENV TZ=Asia/Tokyo

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata \
    && ln -snf /usr/share/zoneinfo/"$TZ" /etc/localtime \
    && echo "$TZ" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV PATH="/opt/airflow/.venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./
COPY dags/ ./dags/
RUN uv sync --frozen --no-dev
