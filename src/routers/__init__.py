from .change_password import router as change_password_router
from .login import router as login_router
from .refresh_token import router as refresh_token_router
from .register import router as register_router
from .resend_email_verification import router as resend_email_verification_router
from .verify_email import router as verify_email_router

routers = [
    change_password_router,
    login_router,
    refresh_token_router,
    register_router,
    resend_email_verification_router,
    verify_email_router,
]
