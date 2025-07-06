from pydantic import BaseModel, EmailStr


class SignInResponseDAO(BaseModel):
    access_token: str
    token_type: str
    status_code: int


class SignInRequestDAO(BaseModel):
    email: EmailStr
    password: str

class UserInfoDAO(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
