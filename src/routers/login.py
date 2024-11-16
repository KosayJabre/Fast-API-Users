from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.database import get_session

from src.users import get_user_by_email, get_user_by_username
from src.utils.auth import create_access_token, create_refresh_token
from src.utils.passwords import verify_password


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class LoginResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: str


@router.post("/api/login", response_model=LoginResponse)
@limiter.limit("3/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    email_or_username = form_data.username
    user_from_email = get_user_by_email(db, email_or_username)
    user_from_username = get_user_by_username(db, email_or_username)

    if user_from_email:
        user = user_from_email
    elif user_from_username:
        user = user_from_username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return LoginResponse(
        message="Login successful", access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id), token_type="bearer"
    )
