#!/bin/sh
set -e

cd /app/services/shortener-service
uv run --package shortener-service --no-dev alembic upgrade head

exec uv run --package shortener-service --no-dev \
  uvicorn shortener_service.main:app --host 0.0.0.0 --port 8002
