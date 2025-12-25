"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getPlayer, registerPlayer } from "@/lib/api";
import AnalyticsTabs from "@/components/AnalyticsTabs";

function formatTime(ts: string) {
  return new Date(ts).toLocaleString();
}

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-500">
        Loading player…
      </div>
    );
  }

  if (!player) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-xl shadow-sm p-8 w-full max-w-md">
          <h1 className="text-xl font-semibold mb-2">Track Player</h1>
          <p className="text-gray-500 mb-6">
            This player is not being tracked yet.
          </p>

          <button
            onClick={async () => {
              await registerPlayer(tag);
              await load();
            }}
            className="
              w-full
              bg-blue-600
              text-white
              py-3
              rounded-lg
              font-medium
              text-sm
              hover:bg-blue-700
              focus:outline-none
              focus:ring-2
              focus:ring-blue-500
              focus:ring-offset-2
            "
          >
            Track Player
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-semibold">Player Dashboard</h1>
          <p className="text-gray-500">{player.player_tag}</p>
        </div>

        {/* Status Card */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          {player.last_polled_at === null && (
            <p className="text-gray-500">
              Waiting for first poll…
            </p>
          )}

          {player.last_polled_at && !player.last_seen_at && (
            <>
              <p className="font-medium text-yellow-600">
                Tracking — no recent battles
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Last checked: {formatTime(player.last_polled_at)}
              </p>
            </>
          )}

          {player.last_seen_at && (
            <>
              <p className="font-medium text-green-600">
                Active
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Last played: {formatTime(player.last_seen_at)}
              </p>
              <p className="text-sm text-gray-500">
                Last updated: {formatTime(player.last_polled_at)}
              </p>
            </>
          )}
        </div>

        {/* Analytics */}
        {player.last_polled_at && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-4">
              Analytics
            </h3>
            <AnalyticsTabs />
          </div>
        )}
      </div>
    </div>
  );
}
