from model.attendee import Attendee


class AttendeeRepo:
    def __init__(self) -> None:
        self._attendees = {}

    def add_attendee(self, name: str, email: str) -> Attendee:
        """
        adds a new attendee to the repo
        overwrites attendee with same id
        """
        attendee = Attendee(name=name, email=email)
        self._attendees[attendee.id] = attendee
        return attendee

    def get_all_attendees(self) -> list[Attendee]:
        """
        returns a list of all attendees currently in the repo
        """
        return list(self._attendees.values())

    def get_attendee_by_id(self, attendee_id: str) -> Attendee | None:
        """
        returns the attendee if found
        otherwise returns none
        """
        return self._attendees.get(attendee_id, None)

    def delete_attendee(self, attendee_id: str) -> bool:
        """
        if found, deletes the attendee and returns true
        returns false otherwise
        """
        found_attendee = self._attendees.get(attendee_id, None)
        if found_attendee is None:
            return False
        del self._attendees[attendee_id]
        return True
