# Shortly

Microservice-based URL shortener with analytics, built with FastAPI and Next.js.

## Architecture

The backend is split into four independent microservices communicating via gRPC, sitting behind an Nginx reverse proxy.

| Service | Description |
|---|---|
| **auth-service** | Registration, login, JWT tokens |
| **shortener-service** | Link creation, custom aliases, QR codes |
| **redirect-service** | Fast HTTP redirects, Redis caching, geo lookup |
| **analytics-service** | Click tracking, stats by country / referrer |

## Tech Stack

**Backend** — Python 3.12, FastAPI, gRPC / Protobuf, SQLAlchemy + asyncpg, Alembic, Redis

**Frontend** — Next.js 16, React 19, Tailwind CSS 4, Zod

**Infra** — Docker Compose, Nginx, PostgreSQL 17, uv workspace

## Quick Start

```bash
cp .env.example .env
docker compose up --build -d
```

The app will be available at `http://localhost`.

## Project Structure

```
shortly/
├── frontend/                  # Next.js app
├── backend/
│   ├── proto/                 # Protobuf definitions
│   ├── libs/shared/           # Shared lib (JWT utils, gRPC stubs)
│   └── services/
│       ├── auth-service/
│       ├── shortener-service/
│       ├── redirect-service/
│       └── analytics-service/
├── nginx/                     # Reverse proxy config
└── docker-compose.yml
```
