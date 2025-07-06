from pydantic import BaseModel


class CalorieResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    source: str
    created_at: str
    updated_at: str


class CalorieRequest(BaseModel):
    dish_name: str = None
    servings: int = None
