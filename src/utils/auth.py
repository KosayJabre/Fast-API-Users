from datetime import datetime, timedelta
from typing import Union

import jwt
from src.config import config

SECRET_KEY = config.secret_key
ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRATION = timedelta(hours=config.access_token_expiration_hours)
REFRESH_TOKEN_EXPIRATION = timedelta(days=config.refresh_token_expiration_hours)
EMAIL_VERIFICATION_TOKEN_EXPIRATION = timedelta(
    hours=config.email_verification_token_expiration_hours
)
PASSWORD_RESET_TOKEN_EXPIRATION = timedelta(
    hours=config.password_reset_token_expiration_hours
)


def create_password_reset_token(email_address: str) -> str:
    return encode_token(
        {
            "email": email_address,
            "purpose": "reset_password",
            "exp": datetime.utcnow() + PASSWORD_RESET_TOKEN_EXPIRATION,
        }
    )


def create_access_token(user_id: str) -> str:
    return encode_token(
        {"sub": user_id, "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRATION}
    )


def create_refresh_token(user_id: str) -> str:
    return encode_token(
        {
            "sub": user_id,
            "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRATION,
            "type": "refresh",
        }
    )


def create_email_verification_token(email_address: str) -> str:
    return encode_token(
        {
            "email": email_address,
            "exp": datetime.utcnow() + EMAIL_VERIFICATION_TOKEN_EXPIRATION,
        }
    )


def encode_token(subject: dict):
    return jwt.encode(subject, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: Union[str, bytes]):
    return jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True}
    )
