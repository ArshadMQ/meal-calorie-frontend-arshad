"use client";
import { create } from "zustand";
import { z } from "zod";
import { UserSchema } from "@/types/validation/auth";

type User = z.infer<typeof UserSchema>;

type SessionState = {
  user: User | null;
  isAuthenticated: boolean;
  setSession: (user: User) => void;
  clearSession: () => void;
};

export const useSession = create<SessionState>((set) => ({
  user: null,
  isAuthenticated: false,
  setSession: (user) => set({ user, isAuthenticated: true }),
  clearSession: () => set({ user: null, isAuthenticated: false }),
}));
