import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.config import settings
from auth_service.database import get_session
from auth_service.schemas import RefreshRequest, TokenPair, UserLogin, UserRegister, UserResponse
from auth_service.service import authenticate_user, create_user, get_user_by_email
from shared.dependencies import require_auth
from shared.jwt import create_access_token, create_refresh_token, decode_token

router = APIRouter()

get_current_user = require_auth(settings.jwt_secret_key, settings.jwt_algorithm)


def _issue_tokens(user_id: str, email: str) -> TokenPair:
    data = {"sub": user_id, "email": email}
    return TokenPair(
        access_token=create_access_token(
            data, settings.jwt_secret_key, settings.jwt_access_token_expire_minutes, settings.jwt_algorithm
        ),
        refresh_token=create_refresh_token(
            data, settings.jwt_secret_key, settings.jwt_refresh_token_expire_days, settings.jwt_algorithm
        ),
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: UserRegister, session: AsyncSession = Depends(get_session)):  # noqa: B008
    existing = await get_user_by_email(session, body.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return await create_user(session, body.email, body.password)


@router.post("/login", response_model=TokenPair)
async def login(body: UserLogin, session: AsyncSession = Depends(get_session)):  # noqa: B008
    user = await authenticate_user(session, body.email, body.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return _issue_tokens(str(user.id), user.email)


@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshRequest):
    try:
        payload = decode_token(body.refresh_token, settings.jwt_secret_key, settings.jwt_algorithm)
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from e

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    return _issue_tokens(payload["sub"], payload["email"])


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: dict = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    user = await get_user_by_email(session, current_user["email"])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
