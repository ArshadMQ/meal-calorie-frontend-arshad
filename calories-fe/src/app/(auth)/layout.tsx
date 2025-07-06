import { Sprout } from "lucide-react";
import Image from "next/image";
import React from "react";

const AuthLayout = ({ children }: { children: React.ReactElement }) => {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="bg-muted/50 relative hidden lg:flex items-center flex-col gap-10 justify-center">
        <div className="absolute top-5 left-6 flex justify-center gap-2 md:justify-start">
          <a href="#" className="flex items-center gap-2 font-medium">
            <div className="bg-primary text-primary-foreground flex size-8 items-center justify-center rounded-md">
              <Sprout className="size-5" />
            </div>
            <h3 className="font-normal">Mealory</h3>
          </a>
        </div>
        <Image src="/login.svg" alt="Image" width={400} height={400} />
        <p className="w-[calc(100%-200px)] text-center text-muted-foreground">Track your daily nutrition intake with precision. Monitor calories, macronutrients, and achieve your health goals.</p>
      </div>
      <div className="flex flex-col gap-4 p-6 md:p-10">
        {/* <div className="flex justify-center gap-2 md:justify-start">
          <a href="#" className="flex items-center gap-2 font-medium">
            <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
              <Sprout className="size-4" />
            </div>
            Mealory
          </a>
        </div> */}
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-sm">{children}</div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
