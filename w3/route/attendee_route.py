from pydantic import ValidationError
from flask import request, jsonify, Blueprint, current_app

from util.error_serializer import serialize_validation_errors
from service.attendee_service import AttendeeService
from schema.attendee_schema import CreateAttendeeSchema
from dto.attendee_dto import CreateAttendeeRequestDto, AttendeeDto

attendees_bp = Blueprint("attendees", __name__, url_prefix="/attendees")


@attendees_bp.post("")
def add_attendee_route():
    attendee_service: AttendeeService = current_app.extensions[
        "services"
    ].attendee_service

    schema: CreateAttendeeSchema | None = None
    try:
        schema = CreateAttendeeSchema.model_validate(request.get_json())
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

    create_attendee_dto = CreateAttendeeRequestDto(
        name=schema.name,
        email=schema.email,
    )

    attendee_created_dto: AttendeeDto = attendee_service.create_attendee(
        create_attendee_dto
    )

    return (
        jsonify({"status": "ok", "data": attendee_created_dto}),
        201,
    )


@attendees_bp.get("")
def get_all_attendees_route():
    attendee_service: AttendeeService = current_app.extensions[
        "services"
    ].attendee_service

    attendees: list[AttendeeDto] = attendee_service.get_all_attendees()

    return jsonify({"status": "ok", "data": attendees}), 200


@attendees_bp.get("/<string:attendee_id>")
def get_attendee_by_id_route(attendee_id: str):
    attendee_service: AttendeeService = current_app.extensions[
        "services"
    ].attendee_service

    found_attendee: AttendeeDto | None = attendee_service.get_attendee_by_id(
        attendee_id
    )

    if found_attendee is None:
        return (
            jsonify({"status": "not_found", "data": {"message": "attendee not found"}}),
            404,
        )

    return jsonify({"status": "ok", "data": found_attendee}), 200


@attendees_bp.delete("/<string:attendee_id>")
def delete_attendee_route(attendee_id: str):
    attendee_service: AttendeeService = current_app.extensions[
        "services"
    ].attendee_service

    deleted = attendee_service.delete_attendee(attendee_id)
    if deleted:
        return jsonify({"status": "ok", "data": {"message": "attendee deleted"}}), 204
    else:
        return (
            jsonify({"status": "not_found", "data": {"message": "attendee not found"}}),
            404,
        )
