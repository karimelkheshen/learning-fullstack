import pytest


@pytest.fixture
def created_task(client, created_user):
    response = client.post(
        "/tasks",
        json={
            "title": "test task",
            "description": "test",
            "owner_id": created_user["id"],
            "status": "todo",
            "priority": "low",
        },
    )

    assert response.status_code == 201

    return response.get_json()["details"]


@pytest.fixture
def created_task_default(client, created_user):
    response = client.post(
        "/tasks",
        json={
            "title": "test task default",
            "description": "test",
            "owner_id": created_user["id"],
        },
    )

    assert response.status_code == 201

    return response.get_json()["details"]


@pytest.fixture
def created_tasks(client, created_user):
    tasks = []

    response = client.post(
        "/tasks",
        json={
            "title": "test task 1",
            "description": "test",
            "owner_id": created_user["id"],
            "status": "todo",
            "priority": "low",
        },
    )

    assert response.status_code == 201
    tasks.append(response.get_json()["details"])

    response = client.post(
        "/tasks",
        json={
            "title": "test task 2",
            "description": "test",
            "owner_id": created_user["id"],
            "status": "done",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    tasks.append(response.get_json()["details"])

    return tasks


def test_task_status_and_priority_serialize_as_strings(created_task):
    assert isinstance(created_task["status"], str)
    assert isinstance(created_task["priority"], str)
    assert created_task["status"] == "todo"
    assert created_task["priority"] == "low"


def test_create_task_valid(client, created_user):
    test_title = "test task"
    test_description = "test description"
    test_owner_id = created_user["id"]
    test_status = "todo"
    test_priority = "low"

    response = client.post(
        "/tasks",
        json={
            "title": test_title,
            "description": test_description,
            "owner_id": test_owner_id,
            "status": test_status,
            "priority": test_priority,
        },
    )

    assert response.status_code == 201

    task = response.get_json()["details"]
    assert task["title"] == test_title
    assert task["description"] == test_description
    assert task["owner_id"] == test_owner_id
    assert task["status"] == test_status
    assert task["priority"] == test_priority
    assert task["id"] is not None
    assert task["created_at"] is not None


def test_create_task_invalid_request(client, created_user):
    test_title = "test task"
    test_owner_id = created_user["id"]
    test_status = "todo"
    test_priority = "low"

    response = client.post(
        "/tasks",
        json={
            "title": test_title,
            "owner_id": test_owner_id,
            "status": test_status,
            "priority": test_priority,
        },
    )

    assert response.status_code == 400


def test_create_task_invalid_user_not_found(client):
    test_title = "test task"
    test_description = "test description"
    test_owner_id = "unknown"
    test_status = "todo"
    test_priority = "low"

    response = client.post(
        "/tasks",
        json={
            "title": test_title,
            "description": test_description,
            "owner_id": test_owner_id,
            "status": test_status,
            "priority": test_priority,
        },
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("status", "invalid_status"),
        ("priority", "invalid_priority"),
    ],
)
def test_create_task_invalid_status_priority(
    client, created_user, field, invalid_value
):
    payload = {
        "title": "test task",
        "description": "test description",
        "owner_id": created_user["id"],
    }
    payload[field] = invalid_value

    response = client.post("/tasks", json=payload)
    assert response.status_code == 400


def test_get_task_found(client, created_task):
    task_id = created_task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200


def test_get_task_not_found(client):
    response = client.get("/tasks/unknown_id")
    assert response.status_code == 404


def test_create_task_correct_defaults(created_task_default):
    assert created_task_default["status"] == "todo"
    assert created_task_default["priority"] == "low"


def test_get_all_tasks(client, created_tasks):
    expected_task_ids = [task["id"] for task in created_tasks]
    response = client.get("/tasks")
    assert response.status_code == 200
    received_tasks = response.get_json()["details"]
    assert received_tasks != []
    received_task_ids = [task["id"] for task in received_tasks]
    assert expected_task_ids == received_task_ids


@pytest.mark.parametrize(
    "filter, value",
    [
        ("status", "done"),
        ("priority", "low"),
    ],
)
def test_get_all_tasks_filter_works(client, created_tasks, filter, value):
    expected_task_ids = [task["id"] for task in created_tasks if task[filter] == value]
    response = client.get("/tasks", query_string={filter: value})
    assert response.status_code == 200
    received_tasks = response.get_json()["details"]
    assert received_tasks != []
    received_task_ids = [task["id"] for task in received_tasks]
    assert expected_task_ids == received_task_ids


def test_get_all_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.get_json()["details"]
    assert tasks == []


@pytest.mark.parametrize(
    "field,invalid_value",
    [
        ("status", "invalid_status"),
        ("priority", "invalid_priority"),
    ],
)
def test_get_all_tasks_invalid_filter(client, field, invalid_value):
    response = client.get("/tasks", query_string={field: invalid_value})
    assert response.status_code == 400


def test_update_task_single_field_updated(client, created_task):
    task_id = created_task["id"]
    old_status = created_task["status"]
    new_title = "new title"
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": new_title,
        },
    )
    assert response.status_code == 200
    updated_task = response.get_json()["details"]
    assert updated_task["title"] == new_title
    assert updated_task["status"] == old_status


def test_update_task_not_found(client):
    response = client.patch("/tasks/unknown", json={"title": "new_title"})
    assert response.status_code == 404


def test_update_task_invalid_task_fields(client, created_task):
    task_id = created_task["id"]
    new_invalid_status = "invalid_status"
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "status": new_invalid_status,
        },
    )
    assert response.status_code == 400


def test_delete_task_found(client, created_task):
    task_id = created_task["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200


def test_delete_task_not_found(client):
    response = client.delete("/tasks/unknown")
    assert response.status_code == 404
