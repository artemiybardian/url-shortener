import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.jwt import decode_token

bearer_scheme = HTTPBearer()


def require_auth(
    secret_key: str,
    algorithm: str = "HS256",
):
    """Factory that returns a FastAPI dependency for JWT-protected endpoints."""

    async def _get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # noqa: B008
    ) -> dict:
        try:
            payload = decode_token(credentials.credentials, secret_key, algorithm)
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            ) from e

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload

    return _get_current_user
