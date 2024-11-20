import uuid

from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from src.config import config


SECRET_KEY = config.secret_key
ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRATION = timedelta(hours=config.access_token_expiration_hours)
REFRESH_TOKEN_EXPIRATION = timedelta(hours=config.refresh_token_expiration_hours)


def create_access_token(user_id: int, version: int) -> str:
    return encode_token(
        {"jti": str(uuid.uuid4()), "sub": user_id, "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRATION, "purpose": "access", "version": version}
    )


def create_refresh_token(user_id: str, version: int) -> str:
    return encode_token(
        {"jti": str(uuid.uuid4()), "sub": user_id, "exp": datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRATION, "purpose": "refresh", "version": version}
    )


def encode_token(subject: dict):
    return jwt.encode(subject, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: Union[str, bytes]):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
