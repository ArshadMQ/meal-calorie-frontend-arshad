import httpx
import os


class CaloriesAPI:
    @staticmethod
    async def fetch_calories(dish_name: str):
        url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            "query": dish_name,
            "pageSize": 1,
            "api_key": os.getenv("USDA_API_KEY")
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if data["foods"]:
                    food = data["foods"][0]
                    name = food.get("description", "unknown").lower()
                    kcal = food.get("foodNutrients", [])
                    calories = next((x["value"] for x in kcal if x["nutrientName"].lower() == "energy"), 0)
                    return name, calories
            return None, 0.0
