from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from src.database import get_session
from src.utils.users import get_current_user, get_user_by_email
from src.utils.email_addresses import is_valid_email_address, normalize_email_address
from src.utils.send_email import send_registration_email


class ResendConfirmationRequest(BaseModel):
    email: str


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/api/resend-email-verification", tags=["register"])
@limiter.limit("30/minute")
def resend_confirmation(
    request: Request,
    user_in: ResendConfirmationRequest,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    try:
        normalized_email = normalize_email_address(user_in.email)
        if not is_valid_email_address(normalized_email):
            raise HTTPException(status_code=400, detail=f"Invalid email address")

        user = get_user_by_email(db, normalized_email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        background_tasks.add_task(send_registration_email, recipient_email=normalized_email)

        return {"message": "Confirmation email sent successfully"}
    except Exception as e:
        raise e
