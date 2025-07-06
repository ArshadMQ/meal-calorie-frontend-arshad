from pydantic import EmailStr
from sqlalchemy.orm import Session

from database.schema import User
from domain.signup.dao import SignUpRequestDAO


class SignUpService:

    @staticmethod
    async def get(db_session: Session = None):
        return db_session.query(User).all()

    @staticmethod
    async def get_by_email(email: EmailStr, db_session: Session = None):
        return db_session.query(User).filter(User.email == email).first()

    @staticmethod
    async def build(attributes: SignUpRequestDAO):
        user = SignUpRequestDAO(**attributes.dict())
        return user

    @staticmethod
    async def create(db_session: Session, user_dao: SignUpRequestDAO):
        user = User(**user_dao.dict(exclude_unset=True))
        db_session.add(user)
        db_session.commit()
        return user

    @staticmethod
    async def build_and_create(attributes: SignUpRequestDAO, db_session: Session = None
                               ) -> User:
        user_dao = await SignUpService.build(attributes=attributes)
        user = await SignUpService.create(db_session=db_session, user_dao=user_dao)
        return user
