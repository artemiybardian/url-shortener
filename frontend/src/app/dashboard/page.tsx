"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createUrl, deleteUrl, listUrls, getMe, getQrUrl } from "@/lib/api";
import { clearTokens, getToken, isLoggedIn } from "@/lib/auth";
import type { Url } from "@/lib/schemas";

export default function DashboardPage() {
  const router = useRouter();
  const [urls, setUrls] = useState<Url[]>([]);
  const [email, setEmail] = useState("");
  const [originalUrl, setOriginalUrl] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const loadUrls = useCallback(async () => {
    const token = getToken();
    if (!token) return;
    try {
      setUrls(await listUrls(token));
    } catch {
      setError("Failed to load URLs");
    }
  }, []);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
      return;
    }
    const token = getToken()!;
    getMe(token)
      .then((user) => setEmail(user.email))
      .catch(() => {
        clearTokens();
        router.replace("/login");
      });
    loadUrls();
  }, [router, loadUrls]);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const token = getToken();
    if (!token) return;
    try {
      await createUrl(token, originalUrl, customCode || undefined);
      setOriginalUrl("");
      setCustomCode("");
      await loadUrls();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create URL");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(code: string) {
    const token = getToken();
    if (!token) return;
    try {
      await deleteUrl(token, code);
      await loadUrls();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete");
    }
  }

  function handleLogout() {
    clearTokens();
    router.push("/login");
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          {email && (
            <p className="text-sm text-gray-500">{email}</p>
          )}
        </div>
        <button
          onClick={handleLogout}
          className="text-sm text-gray-500 underline"
        >
          Logout
        </button>
      </div>

      <form onSubmit={handleCreate} className="space-y-3">
        <input
          type="url"
          placeholder="https://example.com/long-url"
          value={originalUrl}
          onChange={(e) => setOriginalUrl(e.target.value)}
          required
          className="w-full rounded border px-3 py-2"
        />
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Custom code (optional)"
            value={customCode}
            onChange={(e) => setCustomCode(e.target.value)}
            className="flex-1 rounded border px-3 py-2"
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded bg-black px-6 py-2 text-white disabled:opacity-50"
          >
            {loading ? "..." : "Shorten"}
          </button>
        </div>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <div className="space-y-3">
        {urls.length === 0 && (
          <p className="text-sm text-gray-400">No URLs yet</p>
        )}
        {urls.map((url) => (
          <div
            key={url.id}
            className={`flex items-center justify-between rounded border p-3 ${
              !url.is_active ? "opacity-50" : ""
            }`}
          >
            <div className="min-w-0 flex-1">
              <p className="font-mono text-sm font-bold">/{url.short_code}</p>
              <p className="truncate text-sm text-gray-500">
                {url.original_url}
              </p>
            </div>
            <div className="ml-4 flex gap-2">
              <Link
                href={`/stats/${url.short_code}`}
                className="text-xs text-blue-600 underline"
              >
                Stats
              </Link>
              <a
                href={getQrUrl(url.short_code)}
                target="_blank"
                rel="noreferrer"
                className="text-xs text-green-600 underline"
              >
                QR
              </a>
              {url.is_active && (
                <button
                  onClick={() => handleDelete(url.short_code)}
                  className="text-xs text-red-600 underline"
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
