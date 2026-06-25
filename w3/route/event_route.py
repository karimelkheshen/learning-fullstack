from flask import jsonify, request, Blueprint, current_app
from pydantic import ValidationError

from util.error_serializer import serialize_validation_errors
from service.event_service import EventService
from dto.event_dto import (
    CreateEventRequestDto,
    EventDto,
    UpdateEventRequestDto,
    GetAllEventsRequestDto,
    GetAllEventsResponseDto,
)
from schema.event_schema import CreateEventSchema, UpdateEventSchema, GetAllEventsSchema

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.post("")
def add_event_route():
    event_service: EventService = current_app.extensions["services"].event_service

    data = request.get_json()

    schema: CreateEventSchema | None = None
    try:
        schema = CreateEventSchema.model_validate(data)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "status": "validation_error",
                    "data": {"errors": serialize_validation_errors(e)},
                }
            ),
            400,
        )

    request_dto: CreateEventRequestDto = CreateEventRequestDto(
        title=schema.title,
        description=schema.description,
        start_time=schema.start_time,
        max_capacity=schema.max_capacity,
        status=schema.status,
    )

    event_dto: EventDto = event_service.create_event(request_dto)

    return jsonify({"status": "ok", "data": event_dto}), 201


@events_bp.get("/<string:event_id>")
def get_event_by_id_route(event_id: str):
    event_service: EventService = current_app.extensions["services"].event_service
    event_dto: EventDto | None = event_service.get_event_by_id(event_id)
    if event_dto is None:
        return (
            jsonify({"status": "not_found", "data": {"message": "event not found"}}),
            404,
        )
    return jsonify({"status": "ok", "data": event_dto}), 200


@events_bp.get("")
def get_all_events_route():
    event_service: EventService = current_app.extensions["services"].event_service

    data = request.args.to_dict()

    schema: GetAllEventsSchema | None = None
    try:
        schema = GetAllEventsSchema.model_validate(data)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "status": "validation_error",
                    "data": {"errors": serialize_validation_errors(e)},
                }
            ),
            400,
        )

    request_dto = GetAllEventsRequestDto(
        status_filter=schema.status_filter,
        sort_by_start_time_asc=schema.sort_by_start_time_asc,
        page=schema.page,
        per_page=schema.per_page,
    )

    response_dto: GetAllEventsResponseDto = event_service.get_all_events(request_dto)

    return jsonify({"status": "ok", "data": response_dto}), 200


@events_bp.put("<string:event_id>")
def update_event_route(event_id: str):
    event_service: EventService = current_app.extensions["services"].event_service

    data = request.get_json()

    schema: UpdateEventSchema | None = None
    try:
        schema = UpdateEventSchema.model_validate(data)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "status": "validation_error",
                    "data": {"errors": serialize_validation_errors(e)},
                }
            ),
            400,
        )

    update_event_req_dto: UpdateEventRequestDto = UpdateEventRequestDto(
        title=schema.title,
        description=schema.description,
        start_time=schema.start_time,
        max_capacity=schema.max_capacity,
        status=schema.status,
    )

    event_dto: EventDto | None = event_service.update_event(
        event_id, update_event_req_dto
    )

    if event_dto is None:
        return (
            jsonify({"status": "not_found", "data": {"message": "event not found"}}),
            404,
        )

    return jsonify({"status": "ok", "data": event_dto}), 200


@events_bp.delete("/<string:event_id>")
def delete_event_route(event_id: str):
    event_service: EventService = current_app.extensions["services"].event_service

    event_deleted = event_service.delete_event(event_id)
    if event_deleted:
        return jsonify({"status": "ok", "data": {"message": "event deleted"}}), 204
    else:
        return (
            jsonify({"status": "not_found", "data": {"message": "event not found"}}),
            404,
        )
