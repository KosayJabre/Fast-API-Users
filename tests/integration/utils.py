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
    # Register a new user
    response = client.post(
        "/api/register",
        json=PRIMARY_USER_DETAILS,
    )
    assert response.status_code == 200
    assert response.json() == successful_registration

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
    # Register a new user
    response = client.post(
        "/api/register",
        json=SECONDARY_USER_DETAILS,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

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


def try_change_password(client: TestClient, username_or_email: str, old_password: str, new_password: str):
    return client.post(
        "/api/change-password",
        json={"username_or_email": username_or_email, "old_password": old_password, "new_password": new_password},
    )
