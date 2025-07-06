from sqlalchemy.orm import Session
from domain.signin.dao import SignInRequestDAO
from domain.signup.services import SignUpService
from utils.base import BaseController
from utils.common import verify_password, create_access_token
from fastapi import status


class SignInController(BaseController):
    def __init__(self, params: SignInRequestDAO, db_session: Session = None):
        super().__init__()
        self.params = params
        self.db_session = db_session
        self.exist_user = None

    async def __call__(self):
        return await self.invoke()

    async def invoke(self):
        await self.check_user_exist()
        await self.generate_jwt()
        await self.to_response_dao()
        return self

    async def check_user_exist(self):
        self.exist_user = await SignUpService.get_by_email(self.params.email, self.db_session)
        if not self.exist_user:
            await self._set_error(msg="User doesn't exists", code_=status.HTTP_404_NOT_FOUND)
        return self

    async def generate_jwt(self):
        if len(self.errors) > 0 or self.code_:
            return self
        if not verify_password(self.params.password, self.exist_user.password):
            await self._set_error(msg="Invalid Credentials: please check your email and password",
                                  code_=status.HTTP_404_NOT_FOUND)
        token = create_access_token(data={"sub": self.params.email})
        await self._set_response(res={"access_token": token, "token_type": "Bearer"},
                                 message="Successfully logged In.", code_=status.HTTP_200_OK)
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
        if len(self.errors) > 0 or self.code_:
            return self
        return self

    @property
    async def success(self):
        if self.errors:
            return False
        return True
