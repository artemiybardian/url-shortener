"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { getStats, getQrUrl } from "@/lib/api";
import type { Stats } from "@/lib/schemas";

export default function StatsPage() {
  const params = useParams<{ code: string }>();
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getStats(params.code)
      .then(setStats)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load stats")
      );
  }, [params.code]);

  if (error) {
    return (
      <div className="pt-16 text-center">
        <p className="text-[var(--danger)]">{error}</p>
        <Link href="/dashboard" className="mt-4 inline-block text-sm text-[var(--accent)] hover:underline">
          Back to dashboard
        </Link>
      </div>
    );
  }

  if (!stats) {
    return <p className="pt-16 text-center text-[var(--muted)]">Loading...</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">
          /{stats.short_code}
        </h1>
        <Link
          href="/dashboard"
          className="text-sm text-[var(--muted)] transition-colors hover:text-white"
        >
          Back
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-5 text-center shadow-sm">
          <p className="text-3xl font-bold">{stats.total_clicks}</p>
          <p className="mt-1 text-xs text-[var(--muted)]">Total clicks</p>
        </div>
        <div className="flex items-center justify-center rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-5 shadow-sm">
          <img
            src={getQrUrl(stats.short_code)}
            alt="QR Code"
            className="h-20 w-20 rounded"
          />
        </div>
      </div>

      {stats.top_countries.length > 0 && (
        <div className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-5 shadow-sm">
          <h2 className="mb-3 text-sm font-semibold">Top countries</h2>
          <div className="space-y-1.5">
            {stats.top_countries.map((c) => (
              <div
                key={c.country}
                className="flex items-center justify-between rounded-lg bg-[var(--input)] px-3 py-2 text-sm"
              >
                <span>{c.country}</span>
                <span className="font-mono text-xs text-[var(--muted)]">{c.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.top_referrers.length > 0 && (
        <div className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-5 shadow-sm">
          <h2 className="mb-3 text-sm font-semibold">Top referrers</h2>
          <div className="space-y-1.5">
            {stats.top_referrers.map((r) => (
              <div
                key={r.referrer}
                className="flex items-center justify-between rounded-lg bg-[var(--input)] px-3 py-2 text-sm"
              >
                <span className="truncate">{r.referrer}</span>
                <span className="ml-2 font-mono text-xs text-[var(--muted)]">{r.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.recent_clicks.length > 0 && (
        <div className="rounded-xl border border-[var(--card-border)] bg-[var(--card)] p-5 shadow-sm">
          <h2 className="mb-3 text-sm font-semibold">Recent clicks</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-[var(--card-border)] text-xs text-[var(--muted)]">
                  <th className="pb-2 font-medium">IP</th>
                  <th className="pb-2 font-medium">Country</th>
                  <th className="pb-2 font-medium">Referrer</th>
                  <th className="pb-2 font-medium">Time</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_clicks.map((click, i) => (
                  <tr key={i} className="border-b border-[var(--card-border)] last:border-0">
                    <td className="py-2 font-mono text-xs">{click.ip_address}</td>
                    <td className="py-2 text-xs">{click.country || "—"}</td>
                    <td className="max-w-32 truncate py-2 text-xs">{click.referrer || "—"}</td>
                    <td className="py-2 text-xs text-[var(--muted)]">
                      {click.clicked_at
                        ? new Date(click.clicked_at).toLocaleString()
                        : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
