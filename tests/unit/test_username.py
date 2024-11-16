from src.utils.usernames import validate_username, normalize_username


def test_username_normalization():
    assert normalize_username("testusername") == "testusername"
    assert normalize_username("TestUsername") == "testusername"
    assert normalize_username("Test Username") == "testusername"
    assert normalize_username("Test-Username") == "testusername"
    assert normalize_username("Test_Username") == "testusername"
    assert normalize_username("Test.Username") == "testusername"
    assert normalize_username("Test Username  ") == "testusername"
    assert normalize_username("  Test Username") == "testusername"


def test_username_validation():
    assert validate_username("admin").is_valid == False
    assert validate_username("123456").is_valid == False
    assert validate_username("Shit Fuck").is_valid == False
    assert validate_username("this username is too long").is_valid == False
    assert validate_username("s").is_valid == False
    assert validate_username(" spaces ").is_valid == False
    assert validate_username("special@chars").is_valid == False

    assert validate_username("some_valid_username").is_valid == True
