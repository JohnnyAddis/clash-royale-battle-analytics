"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getDeckAnalytics } from "@/lib/api";

export default function AnalyticsDecks() {
  const params = useParams();
  const playerTag = decodeURIComponent(params.tag as string);

  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      const res = await getDeckAnalytics(playerTag);
      setData(res);
      setLoading(false);
    }

    load();
  }, [playerTag]);

  if (loading) {
    return <p className="text-gray-500">Loading deck analytics…</p>;
  }

  if (data.length === 0) {
    return <p className="text-gray-500">No deck data yet.</p>;
  }

  return (
    <div className="space-y-3">
      {data.map(([deckSignature, games, wins, winRate]) => (
  <div
    key={deckSignature}
    className="flex justify-between items-center border rounded-lg px-4 py-2"
  >
    <span className="text-sm font-mono truncate max-w-[60%]">
      {deckSignature}
    </span>
    <span className="text-sm text-gray-600">
      {games} games · {winRate}%
    </span>
  </div>
))}
    </div>
  );
}
