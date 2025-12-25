"use client";

import { useEffect, useState } from "react";
import { getDeckAnalytics } from "@/lib/api";

export default function AnalyticsDecks() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDeckAnalytics().then(d => {
      setData(d);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading deck analytics…</p>;

  return (
    <div>
      <h3>Deck Win Rates</h3>
      <ul>
        {data.map((d, i) => (
          <li key={i}>
            {d.games} games — {d.win_rate}% win rate
          </li>
        ))}
      </ul>
    </div>
  );
}
