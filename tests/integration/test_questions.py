from src.tests.utils import (
    db,
    client,
    add_question,
)


def test_get_questions(client):
    response = client.get("/questions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_question(client):
    response = add_question(client, 2023, 10, 5, "What is the meaning of life?")
    question_id = response.json()["question_id"]
    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    assert response.json()["question_id"] == question_id


def test_add_question(client):
    response = client.post(
        "/questions/", json={"year": 2023, "month": 10, "day": 5, "question": "What is the meaning of life?", "question_type": "multiple_choice"}
    )
    assert response.status_code == 200
    assert "question_id" in response.json()


def test_update_question(client):
    response = add_question(client, 2023, 10, 5, "What is the meaning of life?")
    question_id = response.json()["question_id"]
    response = client.patch(
        f"/questions/{question_id}",
        json={"year": 2023, "month": 10, "day": 6, "question": "What is the purpose of existence?", "question_type": "multiple_choice"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Question updated successfully"


def test_delete_question(client):
    response = add_question(client, 2023, 10, 5, "What is the meaning of life?")
    question_id = response.json()["question_id"]
    response = client.delete(f"/questions/{question_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Question deleted successfully"
