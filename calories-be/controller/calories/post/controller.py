from sqlalchemy.orm import Session
from domain.calories.api import CaloriesAPI
from domain.calories.dao import CalorieResponse, CalorieRequest
from utils.base import BaseController
from fastapi import status
from database.schema import User, Dish
from datetime import datetime


class FetchCaloriesController(BaseController):
    def __init__(self, params: CalorieRequest, login_user: User, db_session: Session = None):
        super().__init__()
        self.params = params
        self.login_user = login_user
        self.db_session = db_session
        self.exist_user = None
        self.dish = None

    async def __call__(self):
        return await self.invoke()

    async def invoke(self):
        await self.check_user_exist()
        await self.check_validation()
        await self.fetch_records()
        await self.to_response_dao()
        return self

    async def check_user_exist(self):
        if (isinstance(self.login_user, dict) and self.login_user.get("status_code") == status.HTTP_401_UNAUTHORIZED):
            await self._set_error(msg="Invalid User", code_=status.HTTP_401_UNAUTHORIZED)
        return self

    async def check_validation(self):
        if self.errors:
            return self

        if not self.params.dish_name:
            await self._set_error(msg="Input dish name", code_=status.HTTP_404_NOT_FOUND)

        if not self.params.servings or self.params.servings <= 0:
            await self._set_error(msg="Input servings", code_=status.HTTP_404_NOT_FOUND)
        return self

    async def fetch_records(self):
        if self.errors:
            return self

        name, cal = await CaloriesAPI.fetch_calories(self.params.dish_name)
        if cal == 0:
            await self._set_error(msg="Dish not found", code_=status.HTTP_404_NOT_FOUND)
        total = cal * self.params.servings
        self.dish = Dish(name=name, servings=self.params.servings, calories_per_serving=cal,
                         source="USDA FoodData Central", total_calories=total, user_id=self.login_user.id)
        self.db_session.add(self.dish)
        self.db_session.commit()
        dao = CalorieResponse(
            dish_name=name,
            servings=self.params.servings,
            calories_per_serving=cal,
            total_calories=total,
            source="USDA FoodData Central",
            created_at=str(datetime.utcnow()),
            updated_at=str(datetime.utcnow()),
        )

        await self._set_response(res=dao.dict(), message="Successfully fetch records", code_=status.HTTP_200_OK)
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
