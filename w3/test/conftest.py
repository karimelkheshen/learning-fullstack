import pytest

from app import create_app


@pytest.fixture
def client():

    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def created_attendee(client):
    payload = {"name": "test", "email": "test@test.com"}
    response = client.post("/attendees", json=payload)
    assert response.status_code == 201

    return response.get_json()["data"]["details"]


@pytest.fixture
def created_attendees(client):
    payload1 = {"name": "test1", "email": "test1@test.com"}
    payload2 = {"name": "test2", "email": "test2@test.com"}
    response1 = client.post("/attendees", json=payload1)
    response2 = client.post("/attendees", json=payload2)
    assert response1.status_code == 201
    assert response2.status_code == 201

    created_attendee_1 = response1.get_json()["data"]["details"]
    created_attendee_2 = response2.get_json()["data"]["details"]

    return [created_attendee_1, created_attendee_2]
