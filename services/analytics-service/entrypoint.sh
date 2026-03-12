#!/bin/sh
set -e

cd /app/services/analytics-service
uv run --package analytics-service --no-dev alembic upgrade head

exec uv run --package analytics-service --no-dev \
  uvicorn analytics_service.main:app --host 0.0.0.0 --port 8004
