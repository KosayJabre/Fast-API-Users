from src.tests.utils import (
    db,
    client,
    add_question,
)


def test_get_question_answers(client):
    # Add a question first
    response = add_question(client, 2023, 10, 5, "What is the meaning of life?")
    question_id = response.json()["question_id"]

    # Add an answer to the question
    response = client.post(f"/questions/{question_id}/answers", json={"answer": "42"})
    assert response.status_code == 200

    # Get answers for the question
    response = client.get(f"/questions/{question_id}/answers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["answer"] == "42"


def test_add_answer(client):
    # Add a question first
    response = add_question(client, 2023, 10, 5, "What is the meaning of life?")
    question_id = response.json()["question_id"]

    # Add an answer to the question
    response = client.post(f"/questions/{int(question_id)}/answers", json={"answer": "42"})
    assert response.status_code == 200
    assert "answer" in response.json()
