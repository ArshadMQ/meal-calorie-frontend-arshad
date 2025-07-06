from pydantic import BaseModel, EmailStr


class SignUpRequestDAO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str