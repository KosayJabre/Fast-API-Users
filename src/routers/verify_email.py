import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from src.database import get_session
from src.utils.users import get_user_by_email
from src.utils.auth import decode_token


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/api/verify-email/{token}", tags=["register"])
@limiter.limit("30/minute")
def confirm_email(request: Request, token: str, db: Session = Depends(get_session)):
    try:
        email_address = decode_token(token)["email"]
        user = get_user_by_email(db, email_address)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.email_confirmed = True
        db.commit()
        return {"message": "Email confirmed successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to decode verification token.")
