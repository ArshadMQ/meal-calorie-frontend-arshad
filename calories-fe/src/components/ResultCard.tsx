"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { Utensils, Flame, Users, Database, TrendingUp, CheckCircle } from "lucide-react";

interface ResultCardData {
  dish_name: string;
  servings: number;
  calories_per_serving: number;
  total_calories: number;
  source: string;
}

interface NutritionCardProps {
  data: ResultCardData;
}

export default function ResultCard({ data }: NutritionCardProps) {
  // Calculate progress percentage (using 2000 as daily recommended calories)
  const dailyCalorieGoal = 2000;
  const calorieProgress = (data?.total_calories / dailyCalorieGoal) * 100;

  return (
    <Card className="w-full overflow-hidden transition-all duration-300 hover:shadow-xl hover:scale-[1.02] group bg-white dark:bg-zinc-900">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-50 rounded-full transition-colors group-hover:bg-orange-100 dark:bg-orange-900/20 dark:group-hover:bg-orange-900/30">
              <Utensils className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-xl font-bold text-gray-900 dark:text-white capitalize leading-tight">{data?.dish_name}</CardTitle>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Verified
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Calorie Information */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Flame className="w-4 h-4 text-red-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Total Calories</span>
            </div>
            <span className="text-2xl font-bold text-gray-900 dark:text-white">{data?.total_calories?.toFixed(0)}</span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
              <span>Daily Goal Progress</span>
              <span>{calorieProgress.toFixed(1)}%</span>
            </div>
            <Progress value={calorieProgress} className="h-2 bg-gray-100 dark:bg-zinc-700" />
          </div>
        </div>

        <Separator />

        {/* Serving Information */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-blue-50 rounded-lg transition-colors hover:bg-blue-100 dark:bg-blue-900/20 dark:hover:bg-blue-900/30">
            <div className="flex items-center justify-center gap-2 mb-2">
              <Users className="w-4 h-4 text-blue-600" />
              <span className="text-xs font-medium text-blue-700 uppercase tracking-wide">Servings</span>
            </div>
            <div className="text-2xl font-bold text-blue-900">{data?.servings}</div>
          </div>

          <div className="text-center p-3 bg-purple-50 rounded-lg transition-colors hover:bg-purple-100 dark:bg-purple-900/20 dark:hover:bg-purple-900/30">
            <div className="flex items-center justify-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-purple-600" />
              <span className="text-xs font-medium text-purple-700 uppercase tracking-wide">Per Serving</span>
            </div>
            <div className="text-2xl font-bold text-purple-900">{data?.calories_per_serving?.toFixed(0)}</div>
          </div>
        </div>

        <Separator />

        {/* Source Information */}
        <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg dark:bg-zinc-800">
          <Database className="w-4 h-4 text-gray-500" />
          <div>
            <div className="text-xs font-medium text-gray-700 dark:text-gray-300">Data Source</div>
            <div className="text-sm text-gray-600 dark:text-gray-300">{data?.source}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
