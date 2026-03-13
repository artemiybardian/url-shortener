import type { Metadata } from "next";
import "./globals.css";
import { Header } from "./header";

export const metadata: Metadata = {
  title: "URL Shortener",
  description: "Shorten, track, and manage your URLs",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[var(--background)] text-[var(--foreground)] antialiased">
        <Header />
        <main className="mx-auto max-w-2xl px-4 py-10">{children}</main>
      </body>
    </html>
  );
}
