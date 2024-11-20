from .utils import (
    client,
    db,
    try_register_user,
)


def test_registration(client):
    # Register a new user
    response = try_register_user(client, {"username": "TestUser", "email": "test@test.com", "password": "SomeReallyStrongPassword123!"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "user_id": 1}

    # Try to register the same user again
    response = try_register_user(client, {"username": "TestUser", "email": "test@test.com", "password": "SomeReallyStrongPassword123!"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

    # Register a different user
    response = try_register_user(client, {"username": "TestUser2", "email": "test2@test.com", "password": "SomeReallyStrongPassword123!"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "user_id": 2}
