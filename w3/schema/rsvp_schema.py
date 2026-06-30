from pydantic import BaseModel


class CreateRsvpSchema(BaseModel):
    attendee_id: str
