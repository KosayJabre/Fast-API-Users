from datetime import datetime, timedelta
from typing import Union

import jwt


SECRET_KEY = "TOP-SECRET-KEY"  # TODO: read this from environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = timedelta(hours=1)
REFRESH_TOKEN_EXPIRATION = timedelta(days=7)
EMAIL_VERIFICATION_TOKEN_EXPIRATION = timedelta(hours=1)
PASSWORD_RESET_TOKEN_EXPIRATION = timedelta(hours=1)


def create_password_reset_token(email_address: str) -> str:
    return encode_token({"email": email_address, "purpose": "reset_password", "exp": datetime.utcnow() + PASSWORD_RESET_TOKEN_EXPIRATION})


def create_access_token(user_id: str) -> str:
    return encode_token({"sub": user_id, "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRATION})


def create_refresh_token(user_id: str) -> str:
    return encode_token({"sub": user_id, "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRATION, "type": "refresh"})


def create_email_verification_token(email_address: str) -> str:
    return encode_token({"email": email_address, "exp": datetime.utcnow() + EMAIL_VERIFICATION_TOKEN_EXPIRATION})


def encode_token(subject: dict):
    return jwt.encode(subject, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: Union[str, bytes]):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
