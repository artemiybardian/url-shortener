FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY libs/shared/ libs/shared/
COPY services/redirect-service/ services/redirect-service/

RUN uv sync --frozen --package redirect-service --no-dev

EXPOSE 8003

CMD ["uv", "run", "--package", "redirect-service", "--no-dev", \
     "uvicorn", "redirect_service.main:app", "--host", "0.0.0.0", "--port", "8003"]
