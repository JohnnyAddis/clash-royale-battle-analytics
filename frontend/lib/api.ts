const API_BASE = "http://localhost:8000";

export async function getPlayer(tag: string) {
  const clean = tag.trim().replace(/^#/, "");
  const normalized = `#${clean}`;

  const res = await fetch(
    `${API_BASE}/players/${encodeURIComponent(normalized)}`
  );

  if (res.status === 404) return null;
  if (!res.ok) throw new Error("Failed to load player");

  return res.json();
}


export async function registerPlayer(tag: string) {
  const clean = tag.trim().replace(/^#/, "");
  const normalized = `#${clean}`;

  const res = await fetch(`${API_BASE}/players/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      player_tag: normalized,
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Failed to register player");
  }

  return res.json();
}


export async function getDeckAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/decks`);
  if (!res.ok) throw new Error("Failed to fetch deck analytics");
  return res.json();
}

export async function getModeAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/modes`);
  if (!res.ok) throw new Error("Failed to fetch mode analytics");
  return res.json();
}

export async function getTimeSeriesAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/timeseries`);
  if (!res.ok) throw new Error("Failed to fetch time series analytics");
  return res.json();
}
