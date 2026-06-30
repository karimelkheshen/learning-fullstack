from flask import Flask, jsonify

from container import ServiceContainer

from repo.attendee_repo import AttendeeRepo
from repo.event_repo import EventsRepo
from repo.rsvp_repo import RsvpRepo

from service.attendee_service import AttendeeService
from service.event_service import EventService
from service.rsvp_service import RsvpService

from route.attendee_route import attendees_bp
from route.event_route import events_bp
from route.rsvp_route import rsvp_bp


def create_app() -> Flask:
    app = Flask(__name__)

    attendee_repo = AttendeeRepo()
    attendee_service = AttendeeService(attendee_repo)

    event_repo = EventsRepo()
    event_service = EventService(event_repo)

    rsvp_repo = RsvpRepo()
    rsvp_service = RsvpService(rsvp_repo, attendee_service, event_service)

    service_container = ServiceContainer(
        attendee_service=attendee_service,
        event_service=event_service,
        rsvp_service=rsvp_service,
    )

    app.extensions["services"] = service_container

    app.register_blueprint(attendees_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(rsvp_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "data": {}}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
