from datetime import UTC, datetime, timedelta

import jwt

DEFAULT_ALGORITHM = "HS256"


def create_access_token(
    data: dict,
    secret_key: str,
    expire_minutes: int = 30,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    payload = {
        **data,
        "exp": datetime.now(UTC) + timedelta(minutes=expire_minutes),
        "type": "access",
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def create_refresh_token(
    data: dict,
    secret_key: str,
    expire_days: int = 7,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    payload = {
        **data,
        "exp": datetime.now(UTC) + timedelta(days=expire_days),
        "type": "refresh",
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(
    token: str,
    secret_key: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> dict:
    """Decode and validate a JWT token. Raises jwt.PyJWTError on failure."""
    return jwt.decode(token, secret_key, algorithms=[algorithm])
