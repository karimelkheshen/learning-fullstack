from flask import jsonify, request, Blueprint, current_app

from service.user import InvalidUserFieldsError, InvalidRequestError

users_blueprint: Blueprint = Blueprint("users", __name__, url_prefix="/users")


@users_blueprint.post("")
def add_user():
    services = current_app.extensions["services_container"]
    data = request.get_json()
    try:
        user = services.user_service.add_user(data)
        return jsonify({"status": "ok", "details": user.model_dump(mode="json")}), 201
    except InvalidRequestError:
        return jsonify({"status": "error", "details": "invalid request format"}), 400
    except InvalidUserFieldsError:
        return jsonify({"status": "error", "details": "invalid user field(s)"}), 400


@users_blueprint.get("/<string:user_id>")
def get_user_by_id(user_id: str):
    services = current_app.extensions["services_container"]
    user = services.user_service.get_user_by_id(user_id)
    if user is None:
        return (
            jsonify({"status": "not found", "details": "user not found"}),
            404,
        )
    return jsonify({"status": "ok", "details": user.model_dump(mode="json")}), 200
