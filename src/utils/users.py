from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.utils.email_addresses import normalize_email_address
from src.tables import User
from src.utils.usernames import normalize_username


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: int) -> User:
    normalized_email = normalize_email_address(email)
    return db.query(User).filter(User.normalized_email == normalized_email).first()


def get_user_by_username(db: Session, username: int) -> User:
    normalized_username = normalize_username(username)
    return db.query(User).filter(User.normalized_username == normalized_username).first()


def get_user_by_username_or_email(db: Session, username_or_email: int) -> User:
    normalized_email = normalize_email_address(username_or_email)
    normalized_username = normalize_username(username_or_email)
    return db.query(User).filter(or_(User.normalized_email == normalized_email, User.normalized_username == normalized_username)).first()
