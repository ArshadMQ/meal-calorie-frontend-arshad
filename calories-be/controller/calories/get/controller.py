from sqlalchemy.orm import Session
from domain.calories.api import CaloriesAPI
from domain.calories.dao import CalorieResponse, CalorieRequest
from utils.base import BaseController
from fastapi import status
from database.schema import User, Dish
from datetime import datetime


class ListCaloriesController(BaseController):
    def __init__(self, login_user: User, db_session: Session = None):
        super().__init__()
        self.login_user = login_user
        self.db_session = db_session
        self.exist_user = None
        self.dish = None

    async def __call__(self):
        return await self.invoke()

    async def invoke(self):
        await self.check_user_exist()
        await self.fetch_records()
        await self.to_response_dao()
        return self

    async def check_user_exist(self):
        if (isinstance(self.login_user, dict) and self.login_user.get("status_code") == status.HTTP_401_UNAUTHORIZED):
            await self._set_error(msg="Invalid User", code_=status.HTTP_401_UNAUTHORIZED)
        return self

    async def fetch_records(self):
        if self.errors:
            return self

        dish = self.db_session.query(Dish).filter(Dish.user_id == self.login_user.id).all()
        dao = [
            CalorieResponse(
                dish_name=d.name,
                servings=d.servings,
                calories_per_serving=d.calories_per_serving,
                total_calories=d.total_calories,
                source=d.source,
                created_at=str(d.created_at),
                updated_at=str(d.updated_at)
            )
            for d in dish
        ]

        await self._set_response(res=[entry.dict() for entry in dao], message="Successfully fetch records", code_=status.HTTP_200_OK)
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
