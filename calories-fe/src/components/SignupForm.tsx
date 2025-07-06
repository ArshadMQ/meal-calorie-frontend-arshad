"use client";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { Eye, EyeOff, LoaderCircle, Router } from "lucide-react";
import { useState } from "react";
import api from "@/lib/axios";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { set } from "zod";

export function SignupForm({ className, ...props }: React.ComponentProps<"form">) {
  const [showPassword, setShowPassword] = useState(false);
  const [isPending, setIsPending] = useState(false);
  const router = useRouter();

  const togglePasswordVisibility = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setShowPassword((prev) => !prev);
  };

  const handleSignup = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const data = {
      first_name: formData.get("firstName"),
      last_name: formData.get("lastName"),
      email: formData.get("email"),
      password: formData.get("password"),
    };

    try {
      setIsPending(true);
      const res = await api.post(`/auth/register`, data);
      if (res.status === 200) {
        toast.success("Account created successfully!", {
          description: "You can now log in with your new account.",
        });
        router.push("/");
      }
      setIsPending(false);
    } catch (err: any) {
      setIsPending(false);
      toast.error("Something went wrong!", {
        description: err.response?.data?.detail || "Please try again after some time.",
      });
      console.error("Signup error:", err.response?.data || err.message);
    }
  };

  return (
    <form onSubmit={handleSignup} autoComplete="off" className={cn("flex flex-col gap-6", className)} {...props}>
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-2xl font-bold">Create new account</h1>
        <p className="text-muted-foreground text-sm text-balance">Enter your details to create a new account</p>
      </div>
      <div className="grid gap-4">
        <div className="flex w-full gap-2 justify-between">
          <div className="flex gap-2 flex-col w-full">
            <Label htmlFor="firstName">First Name</Label>
            <Input id="firstName" name="firstName" type="text" placeholder="Uncle" required />
          </div>
          <div className="flex gap-2 flex-col w-full">
            <Label htmlFor="lastName">Last Name</Label>
            <Input id="lastName" name="lastName" type="text" placeholder="Bob" required />
          </div>
        </div>
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" name="email" type="email" placeholder="unclebob@email.com" required autoComplete="off" autoCorrect="off" />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="password">Password</Label>
          <div className="relative">
            <Input id="password" name="password" type={showPassword ? "text" : "password"} placeholder="Password" required className="pr-10" />
            <Button variant={"link"} onClick={togglePasswordVisibility} className="absolute right-0 top-1/2 -translate-y-1/2 text-muted-foreground">
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </Button>
          </div>
        </div>
        <Button type="submit" className="w-full mt-2" disabled={isPending}>
          {isPending ? (
            <div className="flex items-center gap-0">
              <LoaderCircle className="mr-2 size-4 animate-spin" />
              Creating...
            </div>
          ) : (
            "Create"
          )}
        </Button>
      </div>
      <div className="text-center text-sm">
        Already have an account?{" "}
        <Link href="/" className="underline underline-offset-4">
          Sign in
        </Link>
      </div>
    </form>
  );
}
