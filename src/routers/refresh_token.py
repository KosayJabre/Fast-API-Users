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


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/api/refresh-token", response_model=RefreshTokenResponse)
@limiter.limit("30/minute")
def refresh_token(request: Request, refresh_request: RefreshTokenRequest, db: Session = Depends(get_session)):
    try:
        payload = decode_token(refresh_request.refresh_token)
        user_id = payload.get("sub")
        token_version = payload.get("version")
        purpose = payload.get("purpose")
        if purpose != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token",
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Check if token_version matches
    if token_version != user.token_version:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )

    return RefreshTokenResponse(
        message="Token refresh successful",
        access_token=create_access_token(user.id, user.token_version),
        refresh_token=create_refresh_token(user.id, user.token_version),
    )
