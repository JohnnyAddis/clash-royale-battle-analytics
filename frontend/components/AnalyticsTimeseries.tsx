"use client";

import { useEffect, useState } from "react";
import { getTimeSeriesAnalytics } from "@/lib/api";

export default function AnalyticsTimeseries() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTimeSeriesAnalytics().then(d => {
      setData(d);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading trends…</p>;

  return (
    <div>
      <h3>Win Rate Over Time</h3>
      <ul>
        {data.map((d, i) => (
          <li key={i}>
            {d.date}: {d.win_rate}% ({d.games} games)
          </li>
        ))}
      </ul>
    </div>
  );
}
