"use client";

import { useState } from "react";
import AnalyticsDecks from "./AnalyticsDecks";
import AnalyticsModes from "./AnalyticsModes";
import AnalyticsTimeseries from "./AnalyticsTimeseries";

type Tab = "decks" | "modes" | "timeseries";

export default function AnalyticsTabs() {
  const [tab, setTab] = useState<Tab>("decks");

  return (
    <div style={{ marginTop: 24 }}>
      {/* Tabs */}
      <div style={{ display: "flex", gap: 12, marginBottom: 16 }}>
        <button onClick={() => setTab("decks")}>Decks</button>
        <button onClick={() => setTab("modes")}>Modes</button>
        <button onClick={() => setTab("timeseries")}>Trends</button>
      </div>

      {/* Content */}
      {tab === "decks" && <AnalyticsDecks />}
      {tab === "modes" && <AnalyticsModes />}
      {tab === "timeseries" && <AnalyticsTimeseries />}
    </div>
  );
}
