import re

from better_profanity import profanity
from profanity_check import predict
from pydantic import BaseModel

from src.utils.email_address import is_valid_email_address


MINIMUM_USERNAME_LENGTH = 3
MAXIMUM_USERNAME_LENGTH = 24
# Only allow letters, numbers, spaces, underscores, hyphens and dots
ALLOWED_CHARACTERS_REGEX = re.compile(r"^[a-zA-Z0-9_\.\- ]+$")
RESERVED_NAMES = ["admin", "administrator", "staff", "support", "root"]
USERNAME_MINIMUM_PROFANITY_THRESHOLD = 0.66


class UsernameValidationResult(BaseModel):
    is_valid: bool
    reason: str


def normalize_username(username: str) -> str:
    lowercase = username.lower()
    trimmed = lowercase.strip()
    no_whitespace = "".join(trimmed.split())
    no_underscores = no_whitespace.replace("_", "")
    no_hyphens = no_underscores.replace("-", "")
    no_dots = no_hyphens.replace(".", "")
    return no_dots


def validate_username(username: str) -> UsernameValidationResult:
    if len(username) < MINIMUM_USERNAME_LENGTH:
        return UsernameValidationResult(is_valid=False, reason=f"Username is too short. It must be at least {MINIMUM_USERNAME_LENGTH} characters.")

    if len(username) > MAXIMUM_USERNAME_LENGTH:
        return UsernameValidationResult(is_valid=False, reason=f"Username is too long. It must be at most {MAXIMUM_USERNAME_LENGTH} characters.")

    if username.strip() != username:
        return UsernameValidationResult(is_valid=False, reason=f"Username cannot start or end with whitespace.")

    if not ALLOWED_CHARACTERS_REGEX.match(username):
        return UsernameValidationResult(
            is_valid=False, reason=f"Username contains invalid characters. Only alphanumeric characters, underscores, and hyphens are allowed."
        )

    if username.isdigit():
        return UsernameValidationResult(is_valid=False, reason=f"Username cannot be number-only.")

    if username.lower() in RESERVED_NAMES:
        return UsernameValidationResult(is_valid=False, reason=f"Username is reserved. Please choose another one.")

    if username_might_be_profane(username):
        return UsernameValidationResult(is_valid=False, reason=f"Username might contain profanity.")

    if is_valid_email_address(username):
        return UsernameValidationResult(is_valid=False, reason=f"Username cannot be an email address.")

    return UsernameValidationResult(is_valid=True, reason="Username is valid.")


def username_might_be_profane(username: str) -> bool:
    return profanity.contains_profanity(username) or predict([username])[0] == 1
