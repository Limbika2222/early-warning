"use client"

import { Outlet, useLocation } from "react-router-dom"
import Sidebar from "../navigation/Sidebar"
import Header from "./Header"

export default function AppLayout() {
  const location = useLocation()

  // 🔹 Robust title detection (prevents false matches)
  const getTitle = () => {
    const path = location.pathname.toLowerCase()

    if (path === "/reddit" || path.startsWith("/reddit/")) {
      return "Reddit Intelligence"
    }

    if (path === "/who" || path.startsWith("/who/")) {
      return "WHO Surveillance"
    }

    if (path === "/upload") {
      return "Data Upload"
    }

    return "Google Trends Intelligence"
  }

  return (
    <div className="min-h-screen bg-slate-50">

      {/* 🌟 Main Container */}
      <div className="h-full flex">

        {/* 🔹 Sidebar */}
        <Sidebar />

        {/* 🔹 Main Content */}
        <div className="flex flex-col flex-1 overflow-hidden">

          {/* 🔹 Header */}
          <Header title={getTitle()} />

          {/* 🔹 Page Content */}
          <main className="flex-1 overflow-y-auto p-8">
            <div className="max-w-7xl mx-auto">

              {/* 🔥 CRITICAL: This controls routing */}
              <Outlet />

            </div>
          </main>

        </div>
      </div>
    </div>
  )
}