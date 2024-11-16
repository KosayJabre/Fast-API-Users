from src.tests.utils import (
    PRIMARY_USER_DETAILS,
    successful_registration,
    db,
    client,
    access_token,
    try_register_user,
    try_login,
    try_refresh_token,
    try_change_password,
)
from unittest.mock import patch


def test_registration(client):
    with patch("src.routes.register.send_registration_email") as mock_send_email:  # Mock where it's used, not where it's defined
        # register a new user
        response = try_register_user(client, PRIMARY_USER_DETAILS)
        assert response.status_code == 200
        assert response.json() == successful_registration

        mock_send_email.assert_called_once()

        # try to register the same user again
        response = try_register_user(client, PRIMARY_USER_DETAILS)
        assert response.status_code == 400
        assert response.json() == {"detail": "Email already registered"}


def test_login(client):
    with patch("src.routes.register.send_registration_email") as mock_send_email:  # Mock where it's used, not where it's defined
        # create a new user
        response = try_register_user(client, PRIMARY_USER_DETAILS)

        assert response.status_code == 200
        assert response.json() == successful_registration
        mock_send_email.assert_called_once()
        # try to login with wrong credentials
        response = try_login(client, "test@test.com", "wrongpassword")
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect password"}

        # login with email
        response = try_login(client, "test@test.com", "SomeReallyStrongPassword123!")
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json().get("token_type") == "bearer"


def test_refresh_token(client, db):
    with patch("src.routes.register.send_registration_email") as mock_send_email:  # Mock where it's used, not where it's defined
        # Register a new user
        response = try_register_user(client, PRIMARY_USER_DETAILS)
        assert response.status_code == 200
        assert response.json() == successful_registration
        mock_send_email.assert_called_once()
        # Login with correct credentials
        response = try_login(client, "test@test.com", "SomeReallyStrongPassword123!")
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json().get("token_type") == "bearer"

        # Try to refresh the token
        response = try_refresh_token(client, response.json()["refresh_token"])
        assert response.status_code == 200
        assert "access_token" in response.json()

        # Try to refresh with wrong refresh token
        response = try_refresh_token(client, "wrongRefreshToken")
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token"}


def test_change_password(client, db, access_token):
    # Try to change password with wrong old password
    response = try_change_password(client, access_token, "wrongOldPassword", "NewStrongPassword123!")
    assert response.status_code == 401
    assert response.json() == {"detail": "Old password is incorrect"}

    # Try to change password with weak new password
    response = try_change_password(client, access_token, "SomeReallyStrongPassword123!", "weakpassword")
    assert response.status_code == 400
    assert response.json()["detail"].startswith("Password not strong enough:")

    # Change password with correct old password and strong new password
    response = try_change_password(client, access_token, "SomeReallyStrongPassword123!", "NewStrongPassword123!")
    assert response.status_code == 200
    assert response.json() == {"message": "Password changed successfully"}

    # Try to login with old password
    response = try_login(client, "test@test.com", "SomeReallyStrongPassword123!")
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}

    # Login with new password
    response = try_login(client, "test@test.com", "NewStrongPassword123!")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"
