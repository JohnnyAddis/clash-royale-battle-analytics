"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [tag, setTag] = useState("");
  const router = useRouter();

  return (
    <main style={{ padding: 40 }}>
      <h1>Clash Royale Analytics</h1>

      <input
        placeholder="#ABC123"
        value={tag}
        onChange={e => setTag(e.target.value)}
      />

      <button onClick={() => router.push(`/player/${encodeURIComponent(tag)}`)}>
        Track Player
      </button>
    </main>
  );
}
