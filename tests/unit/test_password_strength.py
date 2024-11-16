from src.utils.passwords import validate_password_strength


def test_short_passwords():
    assert validate_password_strength("").is_valid == False
    assert validate_password_strength("abc").is_valid == False
    assert validate_password_strength("aaaaaa").is_valid == False


def test_passwords_with_weak_sequences():
    assert validate_password_strength("qwertyuiop").is_valid == False
    assert validate_password_strength("1234567890").is_valid == False
    assert validate_password_strength("aaaaaaaaaa").is_valid == False
    assert validate_password_strength("123123123123").is_valid == False


def test_strong_passwords():
    assert validate_password_strength("s8d2jt5Js3Oe!ntb1saMz").is_valid == True
    assert validate_password_strength("Mycoolpass123!").is_valid == True
    assert validate_password_strength("SomeSuperStrongPassword").is_valid == True
