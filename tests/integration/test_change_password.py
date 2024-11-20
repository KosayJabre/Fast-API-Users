from .utils import db, client, access_token, try_login, try_change_password, PRIMARY_USER_DETAILS, try_register_user
from unittest.mock import patch


def test_change_password(client, db):
    # Register a new user
    response = try_register_user(client, PRIMARY_USER_DETAILS)
    assert response.status_code == 200

    # Try to change password with wrong old password
    response = try_change_password(client, PRIMARY_USER_DETAILS["username"], "wrongOldPassword", "NewStrongPassword123!")
    assert response.status_code == 401
    assert response.json() == {"detail": "Old password is incorrect"}

    # Try to change password with weak new password
    response = try_change_password(client, PRIMARY_USER_DETAILS["username"], "SomeReallyStrongPassword123!", "weakpassword")
    assert response.status_code == 400
    assert response.json()["detail"].startswith("Password not strong enough:")

    # Change password with correct old password and strong new password
    response = try_change_password(client, PRIMARY_USER_DETAILS["username"], "SomeReallyStrongPassword123!", "NewStrongPassword123!")
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
