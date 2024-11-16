import os
import uuid
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from src.main import app
from src.database import get_session
from sqlmodel import SQLModel


PRIMARY_USER_DETAILS = {"username": "TestUser", "email": "test@test.com", "password": "SomeReallyStrongPassword123!"}
SECONDARY_USER_DETAILS = {"username": "TestUser2", "email": "test2@test.com", "password": "SomeReallyStrongPassword123!"}


successful_registration = {"message": "User created successfully", "user_id": 1}


@pytest.fixture(scope="function")
def db():
    # create a new database for each test
    db_name = f"test_{uuid.uuid4().hex}.db"
    db_url = f"sqlite:///{db_name}"

    engine = create_engine(db_url, connect_args={"check_same_thread": False})

    TestingSessionLocal = sessionmaker(bind=engine)

    session = TestingSessionLocal()
    SQLModel.metadata.create_all(engine)

    yield session  # this is where the testing happens

    # Cleanup
    session.close()
    SQLModel.metadata.drop_all(bind=session.get_bind())
    engine.dispose()

    # drop the database after the test has completed
    os.remove(db_name)


@pytest.fixture(scope="function")
def client(db):
    # Here, db is an instance of Session that points to a new SQLite DB for each test.
    # We override the get_db dependency to return this session for each request.

    def override_get_session():
        yield db

    app.dependency_overrides[get_session] = override_get_session

    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def access_token(client):
    # Mock where it's used, not where it's defined
    with patch("src.routers.register.send_registration_email") as mock_send_email:
        # Register a new user
        response = client.post(
            "/api/register",
            json=PRIMARY_USER_DETAILS,
        )
        assert response.status_code == 200
        assert response.json() == successful_registration

        mock_send_email.assert_called_once()

        # Login with correct credentials
        response = client.post(
            "/api/login",
            data={"username": "test@test.com", "password": "SomeReallyStrongPassword123!"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json().get("token_type") == "bearer"

        return response.json()["access_token"]


@pytest.fixture(scope="function")
def access_token_secondary(client):
    # Mock where it's used, not where it's defined
    with patch("src.utils.send_email.send_registration_email") as mock_send_email:
        # Register a new user
        response = client.post(
            "/api/register",
            json=SECONDARY_USER_DETAILS,
        )
        assert response.status_code == 200
        assert response.json()["message"] == "User created successfully"

        mock_send_email.assert_called_once()

        # Login with correct credentials
        response = client.post(
            "/api/login",
            data={"username": "test2@test.com", "password": "SomeReallyStrongPassword123!"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json().get("token_type") == "bearer"

        return response.json()["access_token"]


def add_question(client, year, month, day, question):
    return client.post("/questions", json={"year": year, "month": month, "day": day, "question": question, "question_type": "multiple_choice"})


def try_register_user(client: TestClient, user_details: dict):
    return client.post(
        "/api/register",
        json=user_details,
    )


def try_login(client: TestClient, username: str, password: str):
    return client.post(
        "/api/login/",
        data={"username": username, "password": password},
    )


def try_refresh_token(client: TestClient, refresh_token: str):
    return client.post(
        "/api/refresh-token/",
        json={"refresh_token": refresh_token},
    )


def try_change_password(client: TestClient, access_token: str, old_password: str, new_password: str):
    return client.post(
        "/api/change-password",
        json={"old_password": old_password, "new_password": new_password},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_comment(client: TestClient, access_token: str, url: str, comment_text: str, parent_comment_id=None):
    return client.post(
        "/api/comment/",
        json={"url": url, "comment_text": comment_text, "parent_comment_id": parent_comment_id},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_get_comment(client: TestClient, access_token: str, comment_id: int):
    return client.get(
        f"/api/comments/{comment_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_delete_comment(client: TestClient, access_token: str, comment_id: int):
    return client.delete(
        f"/api/comments/{comment_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_get_page_comments(client: TestClient, access_token: str, url: str, page_index: int = 0):
    return client.get(
        f"/api/pages/{url}/comments",
        params={"page_index": page_index},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_edit_comment(client: TestClient, access_token: str, comment_id: int, comment_text: str):
    return client.patch(
        f"/api/comments/{comment_id}/",
        json={"comment_text": comment_text},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_report_comment(client: TestClient, access_token: str, comment_id: int, message: str, reason: str):
    return client.post(
        f"/api/comments/{comment_id}/report",
        json={"message": message, "reason": reason},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_report_user(client: TestClient, access_token: str, user_id: int, message: str, reason: str):
    return client.post(
        f"/api/users/{user_id}/report",
        json={"message": message, "reason": reason},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_get_user(client: TestClient, access_token: str, user_id: int):
    return client.get(
        f"/api/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_get_current_user(client: TestClient, access_token: str):
    return client.get(
        f"/api/users/me/",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_page_vote(client: TestClient, access_token: str, url: str, vote: int):
    return client.post(
        f"/api/pages/{url}/vote",
        json={"vote": vote},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_get_page_votes(client: TestClient, access_token: str, url: str):
    return client.get(
        f"/api/pages/{url}/votes",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_comment_vote(client: TestClient, access_token: str, comment_id: int, vote: int):
    return client.post(
        f"/api/comments/{comment_id}/vote",
        json={"vote": vote},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def try_report_page(client: TestClient, access_token: str, url: str, message: str, reason: str):
    return client.post(
        f"/api/pages/{url}/report",
        json={"message": message, "reason": reason},
        headers={"Authorization": f"Bearer {access_token}"},
    )
