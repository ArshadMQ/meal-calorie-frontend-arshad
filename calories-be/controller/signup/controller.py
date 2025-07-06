from sqlalchemy.orm import Session
from domain.signup.dao import SignUpRequestDAO
from domain.signup.services import SignUpService
from utils.base import BaseController
from fastapi import status

from utils.common import get_password_hash


class SignUpController(BaseController):
    def __init__(self, params: SignUpRequestDAO,
                 db_session: Session = None):
        super().__init__()
        self.params = params
        self.db_session = db_session

    async def __call__(self):
        return await self.invoke()

    async def invoke(self):
        await self.check_user_exists()
        await self.create_user()
        await self.to_response_dao()
        return self

    async def check_user_exists(self):
        exists = await SignUpService.get_by_email(email=self.params.email, db_session=self.db_session)
        if exists:
            await self._set_error("Email already registered", status.HTTP_400_BAD_REQUEST)
        return self

    async def create_user(self):
        if len(self.errors) > 0 or self.code_:
            return self
        await SignUpService.build_and_create(attributes=SignUpRequestDAO(
            first_name=self.params.first_name,
            last_name=self.params.last_name,
            password=get_password_hash(self.params.password),
            email=self.params.email,
        ), db_session=self.db_session)
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

        await self._set_response(res={}, message="Successfully created User",
                                 code_=status.HTTP_201_CREATED)
        return self

    @property
    async def success(self):
        """
           Asynchronously determine whether the operation was successful.

           This method checks whether the `errors` list is empty and whether `error_code` is unset.
           If there are no errors and no error code, the operation is considered successful.

           Returns:
               bool: True if there are no errors and no error code; False otherwise.
           """

        if self.errors:
            return False
        return True
