"use client";

import { useState } from "react";
import { shortenAnonymous } from "@/lib/api";
import Link from "next/link";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await shortenAnonymous(url);
      setResult(`${window.location.origin}/${data.short_code}`);
      setUrl("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  async function handleCopy() {
    if (!result) return;
    await navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="flex flex-col items-center pt-16">
      <h1 className="mb-2 text-3xl font-bold tracking-tight">
        Shorten any URL
      </h1>
      <p className="mb-8 text-[var(--muted)]">
        Paste a link and get a short URL instantly. No sign-up needed.
      </p>

      <div className="w-full rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-6 shadow-sm">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="url"
            placeholder="https://example.com/very-long-url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            className="flex-1 rounded-lg border border-[var(--input-border)] bg-[var(--input)] px-4 py-2.5 text-sm text-white placeholder-[var(--muted)] outline-none transition-all focus:border-[var(--accent)] focus:ring-2 focus:ring-[var(--accent)]/25"
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-[var(--accent-hover)] disabled:opacity-50"
          >
            {loading ? "..." : "Shorten"}
          </button>
        </form>

        {error && (
          <p className="mt-3 text-sm text-[var(--danger)]">{error}</p>
        )}

        {result && (
          <div className="mt-4 flex items-center gap-3 rounded-lg border border-[var(--input-border)] bg-[var(--input)] px-4 py-3">
            <a
              href={result}
              target="_blank"
              rel="noreferrer"
              className="flex-1 truncate font-mono text-sm text-[var(--accent)] hover:underline"
            >
              {result}
            </a>
            <button
              onClick={handleCopy}
              className="shrink-0 rounded-md border border-[var(--input-border)] px-3 py-1.5 text-xs transition-colors hover:bg-[var(--card-border)]"
            >
              {copied ? "Copied!" : "Copy"}
            </button>
          </div>
        )}
      </div>

      <p className="mt-6 text-sm text-[var(--muted)]">
        Want custom links, analytics & QR codes?{" "}
        <Link href="/register" className="text-[var(--accent)] hover:underline">
          Create a free account
        </Link>
      </p>
    </div>
  );
}
