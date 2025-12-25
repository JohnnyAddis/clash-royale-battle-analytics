"use client";

import { useEffect, useState } from "react";
import { getModeAnalytics } from "@/lib/api";

export default function AnalyticsModes() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModeAnalytics().then(d => {
      setData(d);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading mode analytics…</p>;

  return (
    <div>
      <h3>Win Rate by Game Mode</h3>
      <ul>
        {data.map((m, i) => (
          <li key={i}>
            {m.game_mode}: {m.win_rate}% ({m.games} games)
          </li>
        ))}
      </ul>
    </div>
  );
}
