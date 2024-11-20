from .utils import (
    PRIMARY_USER_DETAILS,
    successful_registration,
    db,
    client,
    try_register_user,
    try_login,
)
from unittest.mock import patch


def test_login(client):
    # Register a new user
    response = try_register_user(client, PRIMARY_USER_DETAILS)
    assert response.status_code == 200
    assert response.json() == successful_registration

    # Login with the wrong credentials
    response = try_login(client, PRIMARY_USER_DETAILS["email"], "wrongpassword")
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}

    # Login with correct credentials
    response = try_login(client, PRIMARY_USER_DETAILS["email"], PRIMARY_USER_DETAILS["password"])
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"
