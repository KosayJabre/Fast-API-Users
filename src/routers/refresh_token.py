import jwt
from jwt import ExpiredSignatureError
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from src.database import get_session
from src.utils.users import get_user_by_id
from src.utils.auth import create_access_token, create_refresh_token, decode_token


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: str


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/api/refresh-token", response_model=RefreshTokenResponse, tags=["auth"])
@limiter.limit("30/minute")
def refresh_token(request: Request, refresh_request: RefreshTokenRequest, db: Session = Depends(get_session)):
    try:
        payload = decode_token(refresh_request.refresh_token)
        id = payload.get("sub")
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return RefreshTokenResponse(
        message="Login successful", access_token=create_access_token(user.id), refresh_token=create_refresh_token(user.id), token_type="bearer"
    )
