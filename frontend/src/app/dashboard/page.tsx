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
  const [origin, setOrigin] = useState("");
  const [qrCode, setQrCode] = useState<string | null>(null);

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
    setOrigin(window.location.origin);
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        {email && <p className="text-sm text-[var(--muted)]">{email}</p>}
      </div>

      <div className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-5 shadow-sm">
        <form onSubmit={handleCreate} className="space-y-3">
          <input
            type="url"
            placeholder="https://example.com/long-url"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
            required
            className="w-full rounded-lg border border-[var(--input-border)] bg-[var(--input)] px-3 py-2.5 text-sm text-white placeholder-[var(--muted)] outline-none transition-all focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent)]/25"
          />
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Custom code (optional)"
              value={customCode}
              onChange={(e) => setCustomCode(e.target.value)}
              className="flex-1 rounded-lg border border-[var(--input-border)] bg-[var(--input)] px-3 py-2.5 text-sm text-white placeholder-[var(--muted)] outline-none transition-all focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent)]/25"
            />
            <button
              type="submit"
              disabled={loading}
              className="rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[var(--accent-hover)] disabled:opacity-50"
            >
              {loading ? "..." : "Shorten"}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <p className="text-sm text-[var(--danger)]">{error}</p>
      )}

      <div className="space-y-2">
        {urls.length === 0 && (
          <p className="py-8 text-center text-sm text-[var(--muted)]">
            No links yet. Create your first one above.
          </p>
        )}
        {urls.map((url) => (
          <div
            key={url.id}
            className={`flex items-center justify-between rounded-xl border border-[var(--card-border)] bg-[var(--card)] px-4 py-3 transition-shadow hover:shadow-md ${
              !url.is_active ? "opacity-40" : ""
            }`}
          >
            <div className="min-w-0 flex-1">
              <a
                href={`/${url.short_code}`}
                target="_blank"
                rel="noreferrer"
                className="font-mono text-sm font-medium text-[var(--accent)] hover:underline"
              >
                {origin ? `${origin}/${url.short_code}` : `/${url.short_code}`}
              </a>
              <p className="truncate text-xs text-[var(--muted)]">
                {url.original_url}
              </p>
            </div>
            <div className="ml-3 flex items-center gap-2">
              <Link
                href={`/stats/${url.short_code}`}
                className="rounded-md border border-[var(--input-border)] px-2.5 py-1 text-xs text-[var(--muted)] transition-colors hover:bg-[var(--card-border)] hover:text-white"
              >
                Stats
              </Link>
              <button
                onClick={() => setQrCode(url.short_code)}
                className="rounded-md border border-[var(--input-border)] px-2.5 py-1 text-xs text-[var(--muted)] transition-colors hover:bg-[var(--card-border)] hover:text-white"
              >
                QR
              </button>
              {url.is_active && (
                <button
                  onClick={() => handleDelete(url.short_code)}
                  className="rounded-md border border-[var(--input-border)] px-2.5 py-1 text-xs text-[var(--danger)] transition-colors hover:bg-[var(--danger)]/10"
                >
                  Delete
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {qrCode && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={() => setQrCode(null)}
        >
          <div
            className="rounded-2xl border border-[var(--card-border)] bg-[var(--card)] p-6 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-4 text-center">
              <p className="font-mono text-sm text-[var(--accent)]">
                {origin}/{qrCode}
              </p>
            </div>
            <img
              src={getQrUrl(qrCode)}
              alt="QR Code"
              className="mx-auto h-48 w-48 rounded-lg"
            />
            <button
              onClick={() => setQrCode(null)}
              className="mt-4 w-full rounded-lg border border-[var(--input-border)] py-2 text-sm text-[var(--muted)] transition-colors hover:bg-[var(--card-border)] hover:text-white"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
