"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getTimeSeriesAnalytics } from "@/lib/api";

export default function AnalyticsTimeSeries() {
  const params = useParams();
  const playerTag = decodeURIComponent(params.tag as string);

  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      const res = await getTimeSeriesAnalytics(playerTag);
      setData(res);
      setLoading(false);
    }

    load();
  }, [playerTag]);

  if (loading) {
    return <p className="text-gray-500">Loading time series…</p>;
  }

  if (data.length === 0) {
    return <p className="text-gray-500">No time series data yet.</p>;
  }

  return (
    <div className="space-y-2">
      {data.map((row) => (
        <div
          key={row.date}
          className="flex justify-between text-sm border rounded px-3 py-2"
        >
          <span>{row.date}</span>
          <span>
            {row.games} games · {row.win_rate}%
          </span>
        </div>
      ))}
    </div>
  );
}
