from datetime import datetime, timedelta
import pytest

from repo.event_repo import EventsRepo


def test_create_event_valid(client):
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "max_capacity": 100,
        "status": "open",
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 201


def test_create_event_invalid_format(client):
    invalid_payload = {"invalid_field": "invalid_value"}
    response = client.post("/events", json=invalid_payload)
    assert response.status_code == 400


def test_create_event_invalid_start_time(client):
    invalid_start_time = (datetime.now() - timedelta(hours=1)).isoformat()
    payload = {
        "title": "test",
        "description": "test",
        "start_time": invalid_start_time,
        "max_capacity": 100,
        "status": "open",
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_create_event_invalid_max_capacity(client):
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "max_capacity": -1,
        "status": "open",
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 400


def test_create_event_invalid_status(client):
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "max_capacity": 100,
        "status": "invalid_status",
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 400


def test_create_event_mixed_structural_and_semantic_errors_returns_400(client):
    # missing required key and invalid start time
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "status": "invalid_status",
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 400


def test_get_event_by_id_found(client, created_event):
    expected_event_id = created_event["id"]
    response = client.get(f"/events/{expected_event_id}")
    assert response.status_code == 200
    assert response.get_json()["data"]["id"] == expected_event_id


def test_get_event_by_id_not_found(client):
    response = client.get(f"/events/unknown")
    assert response.status_code == 404


def test_get_all_events_empty(client):
    response = client.get("/events")
    assert response.status_code == 200
    assert response.get_json()["data"]["results"] == []


def test_get_all_events_valid(client, created_events):
    expected_event_ids = [event["id"] for event in created_events]
    response = client.get("/events")
    assert response.status_code == 200
    received_event_ids = [
        event["id"] for event in response.get_json()["data"]["results"]
    ]
    per_page = response.get_json()["data"]["per_page"]
    assert expected_event_ids[:per_page] == received_event_ids


def test_get_all_events_pagination_works(client, created_events):
    """
    ! assumes that the created_events function in conftest creates at least double
    the amount of minimum per_page value defined by EventsRepo
    """
    expected_page = 2
    expected_per_page = EventsRepo.PAGINATION_PER_PAGE_MIN
    all_event_ids = [event["id"] for event in created_events]
    offset = (expected_page - 1) * expected_per_page
    expected_event_ids = all_event_ids[offset : offset + expected_per_page]
    response = client.get(f"/events?page={expected_page}&per_page={expected_per_page}")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["page"] == expected_page
    assert data["per_page"] == expected_per_page
    assert [event["id"] for event in data["results"]] == expected_event_ids


def test_get_all_events_status_filter_invalid(client):
    response = client.get("/events?status_filter=invalid")
    assert response.status_code == 400


def test_get_all_events_status_filter_valid(client, created_events):
    status = "draft"
    expected_event_ids = [
        event["id"] for event in created_events if event["status"] == status
    ]
    response = client.get(f"/events?status_filter={status}&per_page=100")
    assert response.status_code == 200
    received_event_ids = [
        event["id"] for event in response.get_json()["data"]["results"]
    ]
    assert expected_event_ids == received_event_ids


def test_get_all_events_sort_by_start_time_invalid(client):
    response = client.get("/events?sort_by_start_time_asc=invalid")
    assert response.status_code == 400


def test_get_all_events_sort_by_start_time_valid(client, created_events):
    expected_event_ids = [
        event["id"]
        for event in sorted(created_events, key=lambda item: item["start_time"])
    ]
    response = client.get("/events?sort_by_start_time_asc=true")
    received_event_ids = [
        event["id"] for event in response.get_json()["data"]["results"]
    ]
    per_page = response.get_json()["data"]["per_page"]
    assert expected_event_ids[:per_page] == received_event_ids


def test_get_all_events_pagination_correct_defaults(client):
    expected_default_page = 1
    expected_default_per_page = EventsRepo.PAGINATION_PER_PAGE_MIN
    response = client.get("/events")
    assert response.status_code == 200
    assert response.get_json()["data"]["page"] == expected_default_page
    assert response.get_json()["data"]["per_page"] == expected_default_per_page


def test_get_all_events_pagination_correct_clamping_page(client):
    invalid_page = -23
    expected_page_clamped = 1
    response = client.get(f"/events?page={invalid_page}")
    assert response.status_code == 200
    assert response.get_json()["data"]["page"] == expected_page_clamped


@pytest.mark.parametrize(
    "invalid, clamped",
    [
        (EventsRepo.PAGINATION_PER_PAGE_MIN - 1, EventsRepo.PAGINATION_PER_PAGE_MIN),
        (EventsRepo.PAGINATION_PER_PAGE_MAX + 1, EventsRepo.PAGINATION_PER_PAGE_MAX),
    ],
)
def test_get_all_events_pagination_correct_clamping_per_page(client, invalid, clamped):
    response = client.get(f"/events?per_page={invalid}")
    assert response.status_code == 200
    assert response.get_json()["data"]["per_page"] == clamped


def test_update_event_not_found(client):
    payload = {
        "title": "test",
        "description": "test",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "max_capacity": 100,
        "status": "open",
    }
    response = client.put("/events/unknown", json=payload)
    assert response.status_code == 404


def test_update_event_valid(client, created_event):
    payload = {
        "title": "update",
        "description": "update",
        "start_time": (datetime.now() + timedelta(hours=3)).isoformat(),
        "max_capacity": 23,
        "status": "closed",
    }
    response = client.put(f"/events/{created_event['id']}", json=payload)
    assert response.status_code == 200
    assert payload["title"] == response.get_json()["data"]["title"]
    assert payload["description"] == response.get_json()["data"]["description"]
    assert payload["start_time"] == response.get_json()["data"]["start_time"]
    assert payload["max_capacity"] == response.get_json()["data"]["max_capacity"]


def test_update_event_invalid_format(client, created_event):
    invalid_payload = {"title": "update"}
    response = client.put(f"/events/{created_event['id']}", json=invalid_payload)
    assert response.status_code == 400


def test_update_event_invalid_start_time(client, created_event):
    invalid_start_time = (datetime.now() - timedelta(hours=3)).isoformat()
    payload = {
        "title": "update",
        "description": "update",
        "start_time": invalid_start_time,
        "max_capacity": 23,
        "status": "closed",
    }
    response = client.put(f"/events/{created_event['id']}", json=payload)
    assert response.status_code == 422


def test_update_event_invalid_max_capacity(client, created_event):
    payload = {
        "title": "update",
        "description": "update",
        "start_time": (datetime.now() + timedelta(hours=3)).isoformat(),
        "max_capacity": 0,
        "status": "closed",
    }
    response = client.put(f"/events/{created_event['id']}", json=payload)
    assert response.status_code == 400


def test_update_event_invalid_status(client, created_event):
    payload = {
        "title": "update",
        "description": "update",
        "start_time": (datetime.now() - timedelta(hours=3)).isoformat(),
        "max_capacity": 23,
        "status": "invalid_status",
    }
    response = client.put(f"/events/{created_event['id']}", json=payload)
    assert response.status_code == 400


def test_delete_event_found(client, created_event):
    event_id = created_event["id"]
    response = client.delete(f"/events/{event_id}")
    assert response.status_code == 204


def test_delete_event_not_found(client):
    response = client.delete("/events/unknown")
    assert response.status_code == 404
