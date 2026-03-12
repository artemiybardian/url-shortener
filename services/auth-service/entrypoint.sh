#!/bin/sh
set -e

cd /app/services/auth-service
uv run --package auth-service --no-dev alembic upgrade head

exec uv run --package auth-service --no-dev \
  uvicorn auth_service.main:app --host 0.0.0.0 --port 8001
