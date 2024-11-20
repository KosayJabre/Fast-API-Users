from datetime import datetime

from sqlalchemy import Column, DateTime, event
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel

from src.utils.email_addresses import normalize_email_address
from .utils.usernames import normalize_username


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

    email: str = Field(unique=True)
    normalized_email: str = Field(unique=True, index=True)

    username: str = Field(unique=True)
    normalized_username: str = Field(unique=True, index=True)

    hashed_password: str = Field()

    token_version: int = Field(default=1)


@event.listens_for(User.email, "set", retval=True)
def set_normalized_email(target, value, oldvalue, initiator):
    target.normalized_email = normalize_email_address(value)
    return value


@event.listens_for(User.username, "set", retval=True)
def set_normalized_username(target, value, oldvalue, initiator):
    target.normalized_username = normalize_username(value)
    return value
