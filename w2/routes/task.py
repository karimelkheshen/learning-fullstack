from flask import request, jsonify, Blueprint, current_app

from model.task import TaskPriority, TaskStatus
from service.task import (
    InvalidRequestError,
    InvalidTaskFieldsError,
    TaskNotFoundException,
    UserNotFoundException,
)

tasks_blueprint = Blueprint(name="tasks", import_name=__name__, url_prefix="/tasks")


@tasks_blueprint.post("")
def create_task():
    services = current_app.extensions["services_container"]
    data = request.get_json()
    try:
        task = services.task_service.add_task(data)
        return jsonify({"status": "ok", "details": task.model_dump(mode="json")}), 201
    except InvalidRequestError:
        return jsonify({"status": "error", "details": "bad request"}), 400
    except UserNotFoundException:
        return (
            jsonify({"status": "error", "details": "user with owner_id not found"}),
            404,
        )
    except InvalidTaskFieldsError:
        return (
            jsonify({"status": "error", "details": "invalid task creation fields"}),
            400,
        )


@tasks_blueprint.get("/<string:task_id>")
def get_task_by_id(task_id: str):
    services = current_app.extensions["services_container"]
    try:
        task = services.task_service.get_task_by_id(task_id)
        return jsonify({"status": "ok", "details": task.model_dump(mode="json")}), 200
    except TaskNotFoundException:
        return jsonify({"status": "not found", "details": "task not found"}), 404


def _parse_priority_string() -> TaskPriority | None:
    raw = request.args.get("priority", None)
    if not raw:
        return None
    return TaskPriority(raw.lower())


def _parse_status_string() -> TaskStatus | None:
    raw = request.args.get("status", None)
    if not raw:
        return None
    return TaskStatus(raw.lower())


@tasks_blueprint.get("")
def get_all_tasks():
    services = current_app.extensions["services_container"]

    priority_filter: TaskPriority | None = None
    try:
        priority_filter = _parse_priority_string()
    except ValueError:
        return jsonify({"status": "error", "details": "invalid priority filter"}), 400

    status_filter: TaskStatus | None = None
    try:
        status_filter = _parse_status_string()
    except ValueError:
        return jsonify({"status": "error", "details": "invalid status filter"}), 400

    try:
        tasks = services.task_service.get_all_tasks(
            priority_filter,
            status_filter,
        )
        return (
            jsonify(
                {
                    "status": "ok",
                    "details": [task.model_dump(mode="json") for task in tasks],
                }
            ),
            200,
        )
    except InvalidRequestError:
        return jsonify({"status": "error", "details": "invalid request format"}), 400


@tasks_blueprint.patch("/<string:task_id>")
def update_task(task_id: str):
    services = current_app.extensions["services_container"]
    data = request.get_json()
    try:
        task = services.task_service.update_task(task_id, data)
        return jsonify({"status": "ok", "details": task.model_dump(mode="json")}), 200
    except TaskNotFoundException:
        return jsonify({"status": "not found", "details": "task not found"}), 404
    except InvalidRequestError:
        return jsonify({"status": "error", "details": "bad request"}), 400
    except InvalidTaskFieldsError:
        return (
            jsonify({"status": "error", "details": "invalid task creation fields"}),
            400,
        )


@tasks_blueprint.delete("/<string:task_id>")
def delete_task(task_id: str):
    services = current_app.extensions["services_container"]
    if services.task_service.delete_task(task_id):
        return jsonify({"status": "ok", "details": "task deleted"}), 200
    else:
        return jsonify({"status": "not found", "details": "task not found"}), 404
