// src/app/dashboard/error.tsx
"use client";

import { useEffect } from "react";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    // Optionally log the error to a monitoring service
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center h-full p-8 text-center">
      <h2 className="text-2xl font-semibold text-red-600 mb-4">Something went wrong!</h2>
      <p className="mb-4 text-gray-500">{error.message}</p>
      <button onClick={() => reset()} className="bg-primary text-white px-4 py-2 rounded hover:bg-primary/80 transition">
        Try Again
      </button>
    </div>
  );
}
