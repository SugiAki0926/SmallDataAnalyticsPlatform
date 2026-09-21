FROM python:3.12-slim-bookworm

ENV TZ=Asia/Tokyo
ENV DBT_PROFILES_DIR=/workspaces/SmallDataAnalyticsPlatform/transform/dap_dbt/profile

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    postgresql-client \
    tzdata \
    && ln -snf /usr/share/zoneinfo/"$TZ" /etc/localtime \
    && echo "$TZ" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/SmallDataAnalyticsPlatform
