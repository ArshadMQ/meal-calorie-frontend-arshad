"use client";
import { Eye, EyeOff, LoaderCircle } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { loginUser } from "@/app/(auth)/actions";
import { toast } from "sonner";

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [isPending, setIsPending] = useState(false);

  const togglePasswordVisibility = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setShowPassword((prev) => !prev);
  };

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const formData = new FormData(e.currentTarget);

      const data = {
        email: formData.get("email"),
        password: formData.get("password"),
      };

      setIsPending(true);
      const result = await loginUser(data);
      setIsPending(false);

      if (result?.error) {
        toast(result.error, {
          description:
            "There is something wrong with your credentials. Please try again.",
        });
        return;
      }

      console.log("Login success");
      router.push("/dashboard");
    } catch (error) {
      setIsPending(false);
      console.log("Login error-------------:", error);
      toast("Something went wrong!", {
        description: "Please try again after some time.",
      });
    }
  };

  return (
    <form
      onSubmit={handleLogin}
      className={cn("flex flex-col gap-6", className)}
      {...props}
    >
      <div className="flex flex-col items-center gap-2 mb-1 text-center">
        <h1 className="text-2xl font-bold">Login to your account</h1>
        <p className="text-muted-foreground text-sm text-balance">
          Enter your credentials to login
        </p>
      </div>
      <div className="grid gap-4">
        <div className="grid gap-3">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            name="email"
            type="email"
            placeholder="email@example.com"
            required
          />
        </div>
        <div className="grid gap-3">
          <div className="flex items-center">
            <Label htmlFor="password">Password</Label>
          </div>
          <div className="relative">
            <Input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              required
              className="pr-10"
            />
            <Button
              variant={"link"}
              onClick={togglePasswordVisibility}
              className="absolute right-0 top-1/2 -translate-y-1/2 text-muted-foreground"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </Button>
          </div>
        </div>
        <Button type="submit" className="w-full mt-2" disabled={isPending}>
          {isPending ? (
            <div className="flex items-center gap-0">
              <LoaderCircle className="mr-2 size-4 animate-spin" />
              Logging in...
            </div>
          ) : (
            "Login"
          )}
        </Button>
      </div>
      <div className="text-center text-sm">
        Don&apos;t have an account?{" "}
        <Link href="/register" className="underline underline-offset-4">
          Sign up
        </Link>
      </div>
    </form>
  );
}
