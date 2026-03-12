import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from shared.jwt import create_access_token
from shortener_service.config import settings
from shortener_service.database import Base, get_session
from shortener_service.main import app

test_engine = create_async_engine("sqlite+aiosqlite://", echo=False)
test_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)


async def _override_get_session():
    async with test_session_factory() as session:
        yield session


app.dependency_overrides[get_session] = _override_get_session

TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
TEST_USER_EMAIL = "test@example.com"


@pytest.fixture(autouse=True)
async def _setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def auth_headers():
    token = create_access_token(
        {"sub": TEST_USER_ID, "email": TEST_USER_EMAIL},
        settings.jwt_secret_key,
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
