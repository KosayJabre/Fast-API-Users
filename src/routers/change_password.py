from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from src.database import get_session
from src.tables import User
from src.utils.users import get_current_user
from src.utils.passwords import hash_password, validate_password_strength, verify_password


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ChangePasswordResponse(BaseModel):
    pass


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/api/change-password", tags=["user"])
@limiter.limit("30/minute")
def change_password(
    request: Request, change_password_request: ChangePasswordRequest, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
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
    db.commit()

    return {"message": "Password changed successfully"}
