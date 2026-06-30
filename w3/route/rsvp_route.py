from flask import jsonify, Blueprint, current_app

from dto.rsvp_dto import RsvpDto
from service.rsvp_service import RsvpService

rsvp_bp = Blueprint("rsvps", __name__, url_prefix="/rsvps")


@rsvp_bp.get("/<string:rsvp_id>")
def get_rsvp_by_id(rsvp_id: str):
    rsvp_service: RsvpService = current_app.extensions["services"].rsvp_service
    rsvp: RsvpDto | None = rsvp_service.get_rsvp_by_id(rsvp_id)
    if rsvp is None:
        return (
            jsonify({"status": "not_found", "data": {"message": "rsvp not found"}}),
            404,
        )
    return jsonify({"status": "ok", "data": rsvp}), 200


@rsvp_bp.delete("/<string:rsvp_id>")
def cancel_rsvp_route(rsvp_id: str):
    rsvp_service: RsvpService = current_app.extensions["services"].rsvp_service
    found_and_cancelled = rsvp_service.cancel_rsvp(rsvp_id)
    if not found_and_cancelled:
        return (
            jsonify({"status": "not_found", "data": {"message": "rsvp not found"}}),
            404,
        )
    return jsonify({"status": "ok", "data": {"message": "rsvp cancelled"}}), 204
