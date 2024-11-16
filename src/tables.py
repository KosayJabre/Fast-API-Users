from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, event
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlmodel import Field, Session, SQLModel, create_engine, select

from src.utils.email_addresses import is_valid_email_address, normalize_email_address
from .utils.usernames import normalize_username

from sqlalchemy.orm import declarative_base


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, index=True)
    email: str = Field(unique=True)
    normalized_email: str = Field(unique=True, index=True)
    username: str = Field(unique=True)
    normalized_username: str = Field(unique=True, index=True)
    hashed_password: str = Field()
    created_at: datetime = Field(default=func.now())
    is_email_verified: bool = Field(default=False)

    @validates("email")
    def validate_email(self, key, email):
        assert is_valid_email_address(email), "Invalid email address"
        return email


@event.listens_for(User.email, "set", retval=True)
def set_normalized_email(target, value, oldvalue, initiator):
    target.normalized_email = normalize_email_address(value)
    return value


@event.listens_for(User.username, "set", retval=True)
def set_normalized_username(target, value, oldvalue, initiator):
    target.normalized_username = normalize_username(value)
    return value
