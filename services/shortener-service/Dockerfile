FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY libs/shared/ libs/shared/
COPY services/shortener-service/ services/shortener-service/

RUN uv sync --frozen --package shortener-service --no-dev

EXPOSE 8002 50051

COPY services/shortener-service/entrypoint.sh /entrypoint.sh
CMD ["/entrypoint.sh"]
