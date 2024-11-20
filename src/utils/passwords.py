from passlib.context import CryptContext
from password_strength.stats import PasswordStats
from pydantic import BaseModel
from src.config import config


MINIMUM_PASSWORD_LENGTH = config.minimum_password_length
MAXIMUM_PASSWORD_LENGTH = config.maximum_password_length
MINIMUM_PASSWORD_STRENGTH = config.minimum_password_strength


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordValidationResult(BaseModel):
    is_valid: bool
    reason: str


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plaintext_password: str, hashed_password: str) -> bool:
    return password_context.verify(plaintext_password, hashed_password)


def password_strength(password: str) -> float:
    """Return a number from 0-1 representing the strength of the password, where 1 is very strong and 0 is very weak."""
    stats = PasswordStats(password)
    weakness_adjustment = stats.weakness_factor / 3  # How much to penalize for weak sequences and patterns (a third as much as normal)
    strength_adjustment = stats.strength(weak_bits=20)  # How strong the password is from an entropy point of view
    return (1 - weakness_adjustment) * strength_adjustment


def validate_password_strength(password: str) -> PasswordValidationResult:
    if not password:
        return PasswordValidationResult(is_valid=False, reason="Password cannot be empty.")

    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return PasswordValidationResult(
            is_valid=False,
            reason=f"Password must be at least {MINIMUM_PASSWORD_LENGTH} characters long.",
        )

    if len(password) > MAXIMUM_PASSWORD_LENGTH:
        return PasswordValidationResult(
            is_valid=False,
            reason=f"Password must be at most {MAXIMUM_PASSWORD_LENGTH} characters long.",
        )

    strength = password_strength(password)
    if strength < MINIMUM_PASSWORD_STRENGTH:
        return PasswordValidationResult(
            is_valid=False,
            reason="Password is not complex enough. Try making it longer, using different characters (for example numbers and symbols), or not including common sequences of characters.",
        )

    return PasswordValidationResult(is_valid=True, reason="Password is strong.")
