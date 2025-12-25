"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getPlayer, registerPlayer } from "@/lib/api";

export default function PlayerPage() {
  const params = useParams();
  const tag = decodeURIComponent(params.tag as string);

  const [player, setPlayer] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const p = await getPlayer(tag);
    setPlayer(p);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, [tag]);

  if (loading) return <p>Loading…</p>;

  if (!player) {
    return (
      <div>
        <p>Player not tracked yet.</p>
        <button
          onClick={async () => {
            await registerPlayer(tag);
            await load();
          }}
        >
          Register & Track
        </button>
      </div>
    );
  }

  return (
    <div>
      <h2>{player.player_tag}</h2>

      {player.last_polled_at === null && (
        <p>Registered — waiting for first poll…</p>
      )}

      {player.last_polled_at && !player.last_seen_at && (
        <p>Tracking — no recent battles</p>
      )}

      {player.last_seen_at && (
        <p>Active — last played {player.last_seen_at}</p>
      )}
    </div>
  );
}
