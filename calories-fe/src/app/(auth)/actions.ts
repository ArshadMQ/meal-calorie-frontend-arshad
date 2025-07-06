"use server";

import { LoginSchema } from "@/types/validation/auth";
import axios from "axios";
import { cookies } from "next/headers";
import { toast } from "sonner";

export async function loginUser(data: unknown) {
  const result = LoginSchema.safeParse(data);
  if (!result.success) {
    return { error: "Invalid input", issues: result.error.flatten() };
  }

  const { email, password } = result.data;

  try {
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, { email, password });
    if (!res.data.data || !res.data.data.access_token) {
      throw new Error("No access token received from server");
    }
    const { access_token } = res.data.data;

    (await cookies()).set("token", access_token, {
      httpOnly: true,
      secure: true,
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24 * 7,
    });

    return { success: true };
  } catch (err: any) {
    console.error("Login error:", err?.response?.data || err.message);

    return {
      error: err?.response?.data?.detail || "Login failed",
    };
  }
}

export async function logoutUser() {
  (await cookies()).delete("token");
}
