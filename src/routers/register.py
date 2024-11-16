from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session


from src.database import get_session
from src.tables import User
from src.utils.users import get_user_by_email, get_user_by_username
from src.utils.email_addresses import is_valid_email_address, normalize_email_address
from src.utils.passwords import hash_password, validate_password_strength
from src.utils.send_email import send_registration_email
from src.utils.usernames import normalize_username, validate_username


class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str


class RegisterUserResponse(BaseModel):
    message: str
    user_id: int


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/api/register", response_model=RegisterUserResponse, tags=["register"])
@limiter.limit("30/minute")
def register(request: Request, user_in: RegisterUserRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    # Check if email is valid
    normalized_email = normalize_email_address(user_in.email)
    if not is_valid_email_address(normalized_email):
        raise HTTPException(status_code=400, detail=f"Invalid email address")

    # Check if username is valid
    normalized_username = normalize_username(user_in.username)
    username_validation_result = validate_username(normalized_username)
    if not username_validation_result.is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid username: {username_validation_result.reason}")

    # Check if the email already exists
    if get_user_by_email(db, normalized_email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if the username already exists
    if get_user_by_username(db, normalized_username):
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if the password is strong enough
    password_validation_result = validate_password_strength(user_in.password)
    if not password_validation_result.is_valid:
        raise HTTPException(status_code=400, detail=f"Password not strong enough: {password_validation_result.reason}")

    # Create a new user and save
    new_user = User(email=user_in.email, username=user_in.username, hashed_password=hash_password(user_in.password))
    db.add(new_user)
    db.commit()

    # Send the verification email
    background_tasks.add_task(send_registration_email, recipient_email=new_user.email)

    return RegisterUserResponse(message="User created successfully", user_id=new_user.id)
