import { UserSchema } from "@/types/validation/auth";
import { cookies } from "next/headers";
import api from "./axios";
import axios from "axios";

export async function getUserFromServer() {
  const token = (await cookies()).get("token")?.value;
  if (!token) return null;

  try {
    const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
      headers: {
        Authorizations: `Bearer ${token}`,
      },
    });

    const result = UserSchema.safeParse(res.data);

    return { ...res?.data?.data, token };
  } catch (error) {
    console.error("Error fetching user data:", error);
    return null;
  }
}
