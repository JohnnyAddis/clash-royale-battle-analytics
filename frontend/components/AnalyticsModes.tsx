"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getModeAnalytics } from "@/lib/api";

export default function AnalyticsModes() {
  const params = useParams();
  const playerTag = decodeURIComponent(params.tag as string);

  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      const res = await getModeAnalytics(playerTag);
      setData(res);
      setLoading(false);
    }

    load();
  }, [playerTag]);

  if (loading) {
    return <p className="text-gray-500">Loading mode analytics…</p>;
  }

  if (data.length === 0) {
    return <p className="text-gray-500">No mode data yet.</p>;
  }

  return (
    <div className="space-y-3">
      {data.map((mode) => (
        <div
          key={mode.game_mode}
          className="flex justify-between border rounded-lg px-4 py-2"
        >
          <span className="font-medium">{mode.game_mode}</span>
          <span className="text-sm text-gray-600">
            {mode.games} games · {mode.win_rate}%
          </span>
        </div>
      ))}
    </div>
  );
}
