from .utils import (
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


def test_refresh_token(client, db):
    # Register a new user
    response = try_register_user(client, PRIMARY_USER_DETAILS)
    assert response.status_code == 200
    assert response.json() == successful_registration

    # Login with correct credentials
    response = try_login(client, "test@test.com", "SomeReallyStrongPassword123!")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json().get("token_type") == "bearer"

    refresh_token = response.json()["refresh_token"]

    # Try to refresh access token using refresh token
    response = try_refresh_token(client, refresh_token)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    new_refresh_token = response.json()["refresh_token"]
    assert new_refresh_token != refresh_token

    # Refresh again, using the token from the new response
    response = try_refresh_token(client, new_refresh_token)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    # Try to refresh with wrong refresh token
    response = try_refresh_token(client, "wrongRefreshToken")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
