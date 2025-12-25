"use client";

import { useState } from "react";
import AnalyticsDecks from "./AnalyticsDecks";
import AnalyticsModes from "./AnalyticsModes";
import AnalyticsTimeseries from "./AnalyticsTimeseries";

type Tab = "decks" | "modes" | "timeseries";

export default function AnalyticsTabs() {
  const [tab, setTab] = useState<Tab>("decks");

  return (
    <div>
      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6 flex gap-6">
        <button
          onClick={() => setTab("decks")}
          className={`pb-3 text-sm font-medium transition ${
            tab === "decks"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          Decks
        </button>

        <button
          onClick={() => setTab("modes")}
          className={`pb-3 text-sm font-medium transition ${
            tab === "modes"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          Modes
        </button>

        <button
          onClick={() => setTab("timeseries")}
          className={`pb-3 text-sm font-medium transition ${
            tab === "timeseries"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          Trends
        </button>
      </div>

      {/* Content */}
      {tab === "decks" && <AnalyticsDecks />}
      {tab === "modes" && <AnalyticsModes />}
      {tab === "timeseries" && <AnalyticsTimeseries />}
    </div>
  );
}
