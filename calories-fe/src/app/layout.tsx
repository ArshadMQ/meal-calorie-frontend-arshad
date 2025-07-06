import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { getUserFromServer } from "@/lib/auth";
import ClientSessionSync from "@/components/ClientSessionSync";
import { Toaster } from "@/components/ui/sonner";
import { cookies, headers } from "next/headers";
import { redirect } from "next/navigation";
import { ThemeProvider } from "@/components/theme-provider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Mealory",
  description: "Track you daily nutrition and calories intake with Mealory",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const user = await getUserFromServer();
  const cookieStore = cookies();

  const token = (await cookieStore).get("token");
  const pathname = (await headers()).get("x-invoke-path") || "";

  if (token && pathname === "/login") {
    redirect("/dashboard");
  }
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem
          disableTransitionOnChange
        >
          <ClientSessionSync user={user} />
          {children}
        </ThemeProvider>
        <Toaster />
      </body>
    </html>
  );
}
