"use client";
import { LogOut, Sprout } from "lucide-react";
import React from "react";
import { ToggleTheme } from "./ToggleTheme";
import { Separator } from "./ui/separator";
import { useSession } from "@/stores/authStore";
import { useRouter } from "next/navigation";
import { logoutUser } from "@/app/(auth)/actions";
import { Button } from "./ui/button";

const Navbar = () => {
  const { clearSession } = useSession();
  const router = useRouter();

  const handleLogout = async () => {
    await logoutUser();
    clearSession();
    router.push("/");
  };

  return (
    <>
      <div className="flex justify-between m-3 max-w-7xl mx-auto">
        <div>
          <a href="/" className="flex items-center gap-2 font-medium">
            <div className="bg-primary text-primary-foreground flex size-8 items-center justify-center rounded-md">
              <Sprout className="size-5" />
            </div>
            <h3 className="font-normal">Mealory</h3>
          </a>
        </div>
        <div className="flex items-center  justify-end">
          <ToggleTheme />
          <Button variant={"ghost"} onClick={handleLogout} className="ml-4">
            <LogOut className="size-4" />
          </Button>
        </div>
      </div>
      <Separator className="opacity-50" />
    </>
  );
};

export default Navbar;
