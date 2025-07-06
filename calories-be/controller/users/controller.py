from sqlalchemy.orm import Session
from domain.signup.services import SignUpService
from database.schema import User
from utils.base import BaseController
from fastapi import status


class UserMeController(BaseController):
    def __init__(self, user: User, db_session: Session = None):
        super().__init__()
        self.user = user
        self.db_session = db_session
        self.exist_user = None

    async def __call__(self):
        return await self.invoke()

    async def invoke(self):
        await self.check_user_exist()
        await self.to_response_dao()
        return self

    async def check_user_exist(self):
        if (isinstance(self.user, dict) and self.user.get("status_code") == status.HTTP_401_UNAUTHORIZED):
            await self._set_error(msg="Invalid User", code_=status.HTTP_401_UNAUTHORIZED)
            return self

        self.exist_user = await SignUpService.get_by_email(self.user.email, self.db_session)
        if not self.exist_user:
            await self._set_error(msg="User doesn't exists", code_=status.HTTP_404_NOT_FOUND)

        await self._set_response(res={"first_name": self.user.first_name,
                                      "last_name": self.user.last_name,
                                      "email": self.user.email}, message="Successfully fetch user info",
                                 code_=status.HTTP_200_OK)
        return self

    async def to_response_dao(self):
        """
           Asynchronously return the current instance as a response DAO (Data Access Object).

           This method is typically used to finalize and return a structured response object.
           If there are any errors or an error code present, the instance is returned as-is,
           potentially indicating a failed or partial operation.

           Returns:
               self: The current instance, regardless of success or error state.
           """
        if self.errors:
            return self
        return self

    @property
    async def success(self):
        if self.errors:
            return False
        return True
