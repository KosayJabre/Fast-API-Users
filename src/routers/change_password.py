from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from src.database import get_session
from src.tables import User
from src.utils.users import get_user_by_username_or_email
from src.utils.passwords import hash_password, validate_password_strength, verify_password


class ChangePasswordRequest(BaseModel):
    username_or_email: str
    old_password: str
    new_password: str


class ChangePasswordResponse(BaseModel):
    message: str


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/api/change-password", response_model=ChangePasswordResponse)
@limiter.limit("30/minute")
def change_password(request: Request, change_password_request: ChangePasswordRequest, db: Session = Depends(get_session)):
    current_user = get_user_by_username_or_email(db, change_password_request.username_or_email)

    # Check that old password provided is correct
    if not verify_password(change_password_request.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Old password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check that new password is strong enough
    validation_result = validate_password_strength(change_password_request.new_password)
    if not validation_result.is_valid:
        raise HTTPException(status_code=400, detail=f"Password not strong enough: {validation_result.reason}")

    # Update the password
    current_user.hashed_password = hash_password(change_password_request.new_password)
    # Revoke all previous access tokens
    current_user.token_version += 1
    db.commit()

    return ChangePasswordResponse(message="Password changed successfully")
