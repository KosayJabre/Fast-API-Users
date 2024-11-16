from email_validator import validate_email


def is_valid_email_address(email: str) -> bool:
    try:
        validate_email(email, check_deliverability=False)  # check_deliverability=False makes it not require internet
        return True
    except Exception as e:
        return False


def normalize_email_address(email: str) -> str:
    try:
        return validate_email(email, check_deliverability=False).normalized
    except Exception as e:
        return None
