import random
from datetime import datetime, timedelta
import pytest

from repo.event_repo import EventsRepo
from model.event import EventStatus

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

    return response.get_json()["data"]


@pytest.fixture
def created_attendees(client):
    results = []

    for i in range(1, 10):
        payload = {"name": f"test_{i}", "email": f"test{i}@test.com"}
        response = client.post("/attendees", json=payload)
        assert response.status_code == 201
        results.append(response.get_json()["data"])

    return results


@pytest.fixture
def created_event(client):
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "max_capacity": 100,
        "status": EventStatus.OPEN,
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 201

    return response.get_json()["data"]


@pytest.fixture
def created_event_not_open(client):
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "max_capacity": 100,
        "status": EventStatus.CLOSED,
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 201

    return response.get_json()["data"]


@pytest.fixture
def created_events(client):
    results = []

    for i in range(1, 3 * EventsRepo.PAGINATION_PER_PAGE_MIN):
        payload = {
            "title": f"test_{i}",
            "description": f"test_{i}",
            "start_time": (datetime.now() + timedelta(days=i)).isoformat(),
            "max_capacity": 100 + i,
            "status": random.choice(["draft", "open", "closed", "cancelled"]),
        }

        response = client.post("/events", json=payload)

        assert response.status_code == 201

        results.append(response.get_json()["data"])

    return results


@pytest.fixture
def created_rsvp(client, created_event, created_attendee):
    res = client.post(
        f"/events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendee["id"]},
    )

    assert res.status_code == 201
    return res.get_json()["data"]
