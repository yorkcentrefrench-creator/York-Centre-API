from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class DemoRequest(BaseModel):
    name: str
    email: str
    mobile_number: int
    message: str

class EnrollRequest(BaseModel):
    plan: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @field_validator("name", "email", "phone", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v