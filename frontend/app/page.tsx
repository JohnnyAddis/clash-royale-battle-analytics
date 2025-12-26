"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const [tag, setTag] = useState("");
  const router = useRouter();

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!tag.trim()) return;
    router.push(`/player/${encodeURIComponent(tag.trim())}`);
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <form
        onSubmit={submit}
        className="bg-white rounded-xl shadow-sm p-8 w-full max-w-md"
      >
        <h1 className="text-xl font-semibold mb-2">
          Clash Royale Analytics
        </h1>
        <p className="text-gray-500 mb-6">
          Enter a player tag to start tracking.
        </p>

        <input
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          placeholder="#PLAYER_TAG"
          className="
            w-full
            border
            border-gray-300
            rounded-lg
            px-3
            py-2
            mb-4
            text-sm
            focus:outline-none
            focus:ring-2
            focus:ring-blue-500
          "
        />

        <button
          type="submit"
          className="
            w-full
            bg-blue-600
            text-white
            py-3
            rounded-lg
            font-medium
            text-sm
            hover:bg-blue-700
          "
        >
          Track Player
        </button>
      </form>
    </div>
  );
}
