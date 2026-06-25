from datetime import datetime, timedelta
from pydantic import Field, BaseModel, field_validator

from model.event import EventStatus


class CreateEventSchema(BaseModel):
    title: str
    description: str
    start_time: datetime
    max_capacity: int = Field(ge=1)
    status: EventStatus

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime) -> datetime:
        if value < datetime.now() + timedelta(seconds=1):
            raise ValueError("Event start time must be in the future")
        return value


class UpdateEventSchema(BaseModel):
    title: str
    description: str
    start_time: datetime
    max_capacity: int = Field(ge=1)
    status: EventStatus

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime) -> datetime:
        if value < datetime.now() + timedelta(seconds=1):
            raise ValueError("Event start time must be in the future")
        return value


class GetAllEventsSchema(BaseModel):
    status_filter: EventStatus | None = None
    sort_by_start_time_asc: bool | None = None
    page: int | None = None
    per_page: int | None = None
