const API_BASE = "http://localhost:8000";

export async function getPlayer(tag: string) {
  const res = await fetch(`${API_BASE}/players/${encodeURIComponent(tag)}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error("Failed to fetch player");
  return res.json();
}

export async function registerPlayer(tag: string) {
  const res = await fetch(`${API_BASE}/players/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_tag: tag }),
  });
  if (!res.ok) throw new Error("Failed to register player");
  return res.json();
}

export async function getDeckAnalytics() {
  return fetch(`${API_BASE}/analytics/decks`).then(r => r.json());
}
