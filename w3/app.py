from flask import Flask, jsonify

from container import ServiceContainer

from repo.attendee_repo import AttendeeRepo
from service.attendee_service import AttendeeService
from route.attendee_route import attendee_bp


def create_app() -> Flask:
    app = Flask(__name__)

    attendee_repo = AttendeeRepo()
    attendee_service = AttendeeService(attendee_repo)

    service_container = ServiceContainer
    service_container.attendee_service = attendee_service

    app.extensions["services"] = service_container

    app.register_blueprint(attendee_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "data": {}}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
