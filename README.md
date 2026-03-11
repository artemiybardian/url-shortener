# URL Shortener

Microservice-based URL shortener built with Python, FastAPI, and gRPC.

## Architecture

| Service | Port | gRPC | Description |
|---------|------|------|-------------|
| **nginx** | 80 | — | Reverse proxy, single entry point |
| **auth-service** | 8001 | — | Registration, authentication, JWT |
| **shortener-service** | 8002 | 50051 | Short link generation, custom aliases |
| **redirect-service** | 8003 | — | Fast HTTP redirect (high-load optimized) |
| **analytics-service** | 8004 | 50052 | Click stats, geo, referrers |

## Features

- Custom short links
- Click analytics
- Geo tracking
- QR code generation

## Tech Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Inter-service:** gRPC (protobuf)
- **Database:** PostgreSQL (async via SQLAlchemy + asyncpg)
- **Cache:** Redis
- **Migrations:** Alembic
- **Package manager:** uv (workspace)
- **Linter:** ruff
- **Tests:** pytest + pytest-asyncio + httpx
- **Proxy:** nginx
- **Containerization:** Docker Compose

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose

### Local Development

```bash
# Install dependencies
uv sync --all-packages

# Run linter
uv run ruff check .

# Run tests
uv run pytest -v

# Run with Docker Compose
cp .env.example .env
docker compose up --build
```

### Regenerate Proto Stubs

```bash
uv run python -m grpc_tools.protoc \
  -I proto \
  --python_out=libs/shared/src/shared/proto \
  --grpc_python_out=libs/shared/src/shared/proto \
  --pyi_out=libs/shared/src/shared/proto \
  proto/shortener.proto proto/analytics.proto
```

## Project Structure

```
url-shortener/
├── pyproject.toml              # uv workspace + ruff + pytest config
├── docker-compose.yml
├── nginx/nginx.conf            # Reverse proxy config
├── proto/                      # Protobuf definitions
├── libs/shared/                # Shared library (JWT, gRPC stubs)
├── services/
│   ├── auth-service/
│   ├── shortener-service/
│   ├── redirect-service/
│   └── analytics-service/
└── .pre-commit-config.yaml
```
