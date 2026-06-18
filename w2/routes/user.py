from flask import jsonify, request, Blueprint

from repo.in_memory_user_repo import InMemoryUserRepo
from service.user import UserService, InvalidUserFieldsError, InvalidRequestError

_user_repo = InMemoryUserRepo()
_user_service = UserService(_user_repo)

users_blueprint: Blueprint = Blueprint("users", __name__, url_prefix="/users/")


@users_blueprint.post("/")
def add_user():
    data = request.get_json()
    try:
        user = _user_service.add_user(data)
        return jsonify({"status": "ok", "details": user.model_dump(mode="json")}), 201
    except InvalidRequestError:
        return jsonify({"status": "error", "details": "invalid request format"}), 400
    except InvalidUserFieldsError:
        return jsonify({"status": "error", "details": "invalid user field(s)"}), 400


@users_blueprint.get("/<string:user_id>")
def get_user_by_id(user_id: str):
    user = _user_service.get_user_by_id(user_id)
    if user is None:
        return (
            jsonify({"status": "not found", "details": "user with id not found"}),
            404,
        )
    return jsonify({"status": "ok", "details": user.model_dump(mode="json")}), 200
