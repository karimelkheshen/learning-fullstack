from flask import Flask, jsonify

from container import ServiceContainer

from repo.attendee_repo import AttendeeRepo
from repo.event_repo import EventsRepo

from service.attendee_service import AttendeeService
from service.event_service import EventService

from route.attendee_route import attendees_bp
from route.event_route import events_bp


def create_app() -> Flask:
    app = Flask(__name__)

    attendee_repo = AttendeeRepo()
    attendee_service = AttendeeService(attendee_repo)

    event_repo = EventsRepo()
    event_service = EventService(event_repo)

    service_container = ServiceContainer
    service_container.attendee_service = attendee_service
    service_container.event_service = event_service

    app.extensions["services"] = service_container

    app.register_blueprint(attendees_bp)
    app.register_blueprint(events_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "data": {}}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
