const API_BASE = "http://localhost:8000";

function normalizeTag(tag: string) {
  const clean = tag.trim().replace(/^#/, "");
  return `#${clean}`;
}

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


export async function getDeckAnalytics(playerTag: string) {
  const res = await fetch(
    `${API_BASE}/analytics/decks/${encodeURIComponent(playerTag)}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch deck analytics");
  }

  return res.json();
}

export async function getModeAnalytics(playerTag: string) {
  const normalized = normalizeTag(playerTag);

  const res = await fetch(
    `${API_BASE}/analytics/modes?player_tag=${encodeURIComponent(normalized)}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch mode analytics");
  }

  return res.json();
}


export async function getTimeSeriesAnalytics(playerTag: string) {
  const normalized = normalizeTag(playerTag);

  const res = await fetch(
    `${API_BASE}/analytics/timeseries?player_tag=${encodeURIComponent(normalized)}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch time series analytics");
  }

  return res.json();
}

