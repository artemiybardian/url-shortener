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
      <div className="space-y-4 pt-16">
        <p className="text-red-600">{error}</p>
        <Link href="/dashboard" className="text-sm underline">
          Back
        </Link>
      </div>
    );
  }

  if (!stats) {
    return <p className="pt-16 text-gray-500">Loading stats...</p>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">/{stats.short_code}</h1>
        <Link href="/dashboard" className="text-sm text-gray-500 underline">
          Back
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="rounded border p-4 text-center">
          <p className="text-3xl font-bold">{stats.total_clicks}</p>
          <p className="text-sm text-gray-500">Total clicks</p>
        </div>
        <div className="flex items-center justify-center rounded border p-4">
          <img
            src={getQrUrl(stats.short_code)}
            alt="QR Code"
            className="h-24 w-24"
          />
        </div>
      </div>

      {stats.top_countries.length > 0 && (
        <div>
          <h2 className="mb-2 font-semibold">Top countries</h2>
          <div className="space-y-1">
            {stats.top_countries.map((c) => (
              <div
                key={c.country}
                className="flex justify-between rounded bg-gray-100 px-3 py-1 text-sm"
              >
                <span>{c.country}</span>
                <span className="font-mono">{c.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.top_referrers.length > 0 && (
        <div>
          <h2 className="mb-2 font-semibold">Top referrers</h2>
          <div className="space-y-1">
            {stats.top_referrers.map((r) => (
              <div
                key={r.referrer}
                className="flex justify-between rounded bg-gray-100 px-3 py-1 text-sm"
              >
                <span className="truncate">{r.referrer}</span>
                <span className="ml-2 font-mono">{r.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.recent_clicks.length > 0 && (
        <div>
          <h2 className="mb-2 font-semibold">Recent clicks</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b text-gray-500">
                  <th className="py-1">IP</th>
                  <th className="py-1">Country</th>
                  <th className="py-1">Referrer</th>
                  <th className="py-1">Time</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_clicks.map((click, i) => (
                  <tr key={i} className="border-b">
                    <td className="py-1 font-mono text-xs">
                      {click.ip_address}
                    </td>
                    <td className="py-1">{click.country || "—"}</td>
                    <td className="max-w-32 truncate py-1">
                      {click.referrer || "—"}
                    </td>
                    <td className="py-1 text-xs text-gray-500">
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
