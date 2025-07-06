import React from "react";
import ResultCard from "./ResultCard";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import axios from "axios";
import { toast } from "sonner";
import api from "@/lib/axios";

const MealForm = ({ setNutritionData, user }: { setNutritionData: any; user: any }) => {
  const [isPending, setIsPending] = React.useState(false);
  const data = [
    {
      dish_name: "Grilled Chicken",
      servings: 2,
      calories_per_serving: 250,
      total_calories: 500,
      source: "Food API",
      created_at: "2025-07-01T10:00:00Z",
      updated_at: "2025-07-05T12:00:00Z",
    },
  ];

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const formData = new FormData(e.currentTarget);

      const data = {
        dish_name: formData.get("dish_name"),
        servings: formData.get("servings"),
      };

      setIsPending(true);
      const result = await api.post("/get-calories", data, {
        headers: {
          "Content-Type": "application/json",
          Authorizations: `Bearer ${user.token}`,
        },
      });
      setIsPending(false);
      setNutritionData(result.data.data);
      console.log("Result from API:", result.data);
    } catch (error) {
      setIsPending(false);
      console.error("Error fetching calories data:", error);
      toast("Failed to fetch calories data. Please try again later.");
    }
  };
  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="flex mb-2 gap-2 ">
        <Input id="dish_name" className="w-[700px]" name="dish_name" type="text" placeholder="Enter dish name" required />
        <Input id="servings" className="w-[400px]" name="servings" type="number" placeholder="Enter servings" required />
        <Button type="submit" disabled={isPending}>
          Check
        </Button>
      </form>
    </div>
  );
};

export default MealForm;
