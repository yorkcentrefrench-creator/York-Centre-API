from pydantic import BaseModel, EmailStr

class DemoRequest(BaseModel):
    name: str
    email: str
    mobile_number: int
    message: str

class EnrollRequest(BaseModel):
    plan: str
    name: str
    email: EmailStr
    phone: str