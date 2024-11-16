from sqlalchemy import Boolean, Column, DateTime, Integer, String, event
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlmodel import SQLModel

from src.utils.email_address import is_valid_email_address, normalize_email_address
from .utils.usernames import normalize_username


from sqlalchemy.orm import declarative_base


class User(SQLModel, table=True):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    normalized_email = Column(String(255), index=True)
    username = Column(String(32), unique=True, index=True)
    normalized_username = Column(String(32), index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_email_verified = Column(Boolean, default=False)

    # Answers made by the user
    answers = relationship("AnswersTable", back_populates="user")

    @validates("email")
    def validate_email(self, key, email):
        assert is_valid_email_address(email), "Invalid email address"
        return email

    def to_user_data(self) -> UserData:
        return UserData(id=str(self.id), email=self.email, username=self.username, is_email_verified=self.is_email_verified)


@event.listens_for(User.email, "set", retval=True)
def set_normalized_email(target, value, oldvalue, initiator):
    target.normalized_email = normalize_email_address(value)
    return value


@event.listens_for(User.username, "set", retval=True)
def set_normalized_username(target, value, oldvalue, initiator):
    target.normalized_username = normalize_username(value)
    return value
