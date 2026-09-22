FROM python:3.12-slim-bookworm
ENV TZ=Asia/Tokyo

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata \
    && ln -snf /usr/share/zoneinfo/"$TZ" /etc/localtime \
    && echo "$TZ" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dap_dbt
ENV PATH="/opt/dap_dbt/.venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV DBT_PROFILES_DIR=/opt/dap_dbt/profile

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-dev
COPY ./ ./

CMD ["dbt", "build", "--target", "prod"]
