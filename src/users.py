from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.database import get_db
from src.utils.email_address import normalize_email_address
from .tables import User
from src.utils.auth import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")


async def try_get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User | Exception:
    try:
        return await get_current_user(token, db)
    except Exception as e:
        return e


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("TRYING TO DECODE TOKEN")
        print(token)
        payload = decode_token(token)
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: int) -> User:
    normalized_email = normalize_email_address(email)
    return db.query(User).filter(User.normalized_email == normalized_email).first()


def get_user_by_username(db: Session, username: int) -> User:
    normalized_username = normalized_username(username)
    return db.query(User).filter(User.normalized_username == normalized_username).first()
