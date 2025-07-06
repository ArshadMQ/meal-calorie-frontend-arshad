"use client";
import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import { toast } from "sonner";

import { Dish, DishTable } from "@/components/DishTable";
import MealForm from "@/components/MealForm";
import ResultCard from "@/components/ResultCard";
import api from "@/lib/axios";
import EmptyCard from "@/components/EmptyCard";
import { Separator } from "@/components/ui/separator";
import { useSession } from "@/stores/authStore";

const DashboardPage = () => {
  const [nutritionData, setNutritionData] = useState<Dish>();
  const { user } = useSession();

  return (
    <div className="max-w-7xl mx-auto mt-10 px-4">
      <h1 className="text-2xl font-semibold mb-6">Calories Table</h1>
      <div className="flex gap-4 items-stretch min-h-[500px] space-x-4 text-sm rounded-lg shadow-md border border-muted p-7 bg-muted/20">
        <div className="md:w-[40%] w-full flex flex-col gap-2">
          <MealForm setNutritionData={setNutritionData} user={user} />
          {nutritionData ? <ResultCard data={nutritionData} /> : <EmptyCard />}
        </div>
        <div className="md:w-[60%] w-full">
          <h1 className="font-bold text-xl">History</h1>
          <DishTable user={user} nutritionData={nutritionData} />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
