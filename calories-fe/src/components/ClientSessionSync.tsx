"use client";

import { useEffect } from "react";
import { useSession } from "@/stores/authStore";

export default function ClientSessionSync({ user }: { user: any }) {
  const { setSession, isAuthenticated } = useSession();

  useEffect(() => {
    if (user && !isAuthenticated) {
      setSession(user);
    }
  }, [user, isAuthenticated]);

  return null;
}
