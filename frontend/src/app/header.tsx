"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { isLoggedIn, clearTokens } from "@/lib/auth";
import { useEffect, useState } from "react";

export function Header() {
  const pathname = usePathname();
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    setLoggedIn(isLoggedIn());
  }, [pathname]);

  function handleLogout() {
    clearTokens();
    setLoggedIn(false);
    window.location.href = "/";
  }

  return (
    <header className="border-b border-[var(--card-border)]">
      <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-lg font-semibold tracking-tight">
          Shortly
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          {loggedIn ? (
            <>
              {pathname !== "/dashboard" && (
                <Link
                  href="/dashboard"
                  className="text-[var(--muted)] transition-colors hover:text-white"
                >
                  Dashboard
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="text-[var(--muted)] transition-colors hover:text-white"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-[var(--muted)] transition-colors hover:text-white"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="rounded-lg bg-[var(--accent)] px-3 py-1.5 text-white transition-colors hover:bg-[var(--accent-hover)]"
              >
                Sign Up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
