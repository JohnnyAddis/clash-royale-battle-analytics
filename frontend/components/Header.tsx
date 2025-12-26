"use client";

import Link from "next/link";

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        <Link
          href="/"
          className="font-semibold text-gray-900 hover:text-blue-600"
        >
          Clash Royale Analytics
        </Link>

        <Link
          href="/"
          className="
            text-sm
            font-medium
            text-blue-600
            hover:text-blue-700
          "
        >
          Track another player
        </Link>
      </div>
    </header>
  );
}
