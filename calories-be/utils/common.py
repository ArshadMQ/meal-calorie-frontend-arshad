from typing import Optional, Dict, Any
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import Header
from fastapi import status
from jwt import PyJWTError
from database.config import cfg
from database.schema import User
from database.connection import SessionLocal

API_VERSION = 1.0
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_session = SessionLocal()
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ERROR_EMAIL_PASSWORD_IS_INCORRECT = "Please login with this correct email and password instead."


def success_response(
        payload: Dict[str, Any], code: int, msg: str = None
) -> Dict[str, Any]:
    return {
        "api_version": API_VERSION,
        "response": {"code": code, "msg": msg},
        "data": payload,
    }


def failure_response(
        code_: int, message: str = "", payload: Optional[Dict[str, Any]] = {}
) -> Dict[str, Any]:
    return {
        "api_version": API_VERSION,
        "errors": {"code": code_, "msg": message},
        "data": payload,
    }


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, cfg("JWT_SECRET"), algorithm=cfg("ALGORITHM"))


class AuthService:
    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, cfg("JWT_SECRET"), algorithms=[cfg("ALGORITHM")])
            email: str = payload.get("sub")
            if email is None:
                return {
                    "errors": ERROR_EMAIL_PASSWORD_IS_INCORRECT,
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
            return email
        except PyJWTError:
            return {
                "errors": ERROR_EMAIL_PASSWORD_IS_INCORRECT,
                "status_code": status.HTTP_404_NOT_FOUND,
            }

    @staticmethod
    async def verify(token: str):
        """Given a JWT it finds the current loggedIn session and returns the user id"""
        try:
            email = AuthService.verify_token(token)
            user_instance = db_session.query(User).filter(User.email == email).one_or_none()
            return user_instance
        except Exception as _:
            return {
                "errors": "Invalid Token",
                "status_code": status.HTTP_401_UNAUTHORIZED
            }
        finally:
            db_session.close()


async def current_user(authorizations: str = Header(None)):
    if not authorizations:
        return {"errors": "Unauthorized", "status_code": status.HTTP_401_UNAUTHORIZED}
    token = authorizations.split()[-1]
    user = await AuthService.verify(token=token)
    if not user:
        return {"errors": "Unauthorized", "status_code": status.HTTP_401_UNAUTHORIZED}
    return user
