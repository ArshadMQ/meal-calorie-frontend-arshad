import { Container } from "lucide-react";
import React from "react";
import { Card } from "./ui/card";

const EmptyCard = () => {
  return (
    <div className="flex items-center justify-center flex-col gap-3 h-full w-full">
      <Container className="size-10 text-primary" />
      <h1 className="font-bold">No data</h1>
      <p className="text-muted-foreground text-center text-xs w-[70%]">Check your meal calories by adding dish name and servings from the above.</p>
    </div>
  );
};

export default EmptyCard;
