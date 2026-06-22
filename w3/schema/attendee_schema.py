from pydantic import BaseModel, Field, EmailStr


class CreateAttendeeSchema(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
