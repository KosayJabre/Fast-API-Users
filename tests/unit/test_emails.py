from src.utils.email_address import is_valid_email_address, normalize_email_address


def test_is_valid_email_address():
    assert is_valid_email_address("test@example.com") == True
    assert is_valid_email_address("invalid-email") == False
    assert is_valid_email_address("test@example") == False
    assert is_valid_email_address("test@.com") == False


def test_normalize_email_address():
    assert normalize_email_address("TEST@Example.COM") == "TEST@example.com"
    assert normalize_email_address("INVALID-EMAIL") == None
    assert normalize_email_address("test@example") == None
