"use client"

import { useEffect, useState } from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts"

// ---------------- TYPES ----------------

interface RedditResponse {
  source: string
  data: Record<string, number>
}

interface ChartData {
  name: string
  value: number
}

// ---------------- COMPONENT ----------------

export default function RedditDashboard() {
  const [data, setData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(true)

  // -------------------------------------------------
  // FETCH REDDIT DATA
  // -------------------------------------------------
  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true)

        const res = await fetch(
          `${import.meta.env.VITE_API_BASE}/api/reddit/symptoms`
        )

        const json: RedditResponse = await res.json()

        const formatted: ChartData[] = Object.entries(json.data || {})
          .map(([symptom, count]) => ({
            name: symptom,
            value: count,
          }))
          .sort((a, b) => b.value - a.value)
          .slice(0, 10) // top 10

        setData(formatted)

      } catch (err) {
        console.error("❌ Reddit load error:", err)
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  // -------------------------------------------------
  // UI
  // -------------------------------------------------
  return (
    <div className="bg-[#F8FAFC] min-h-screen p-6 space-y-6">

      {/* HEADER */}
      <h1 className="text-xl font-semibold">
        Reddit Health Signals Dashboard
      </h1>

      {/* METRIC */}
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <p className="text-sm text-gray-500">Total Signals</p>
        <p className="text-2xl font-semibold">
          {data.reduce((acc, d) => acc + d.value, 0)}
        </p>
      </div>

      {/* CHART */}
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <h2 className="text-sm mb-3 text-gray-600">
          Top Symptoms (Reddit)
        </h2>

        {loading ? (
          <p className="text-gray-400 text-sm">Loading...</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid stroke="#E5E7EB" />

              <XAxis
                dataKey="name"
                angle={-35}
                textAnchor="end"
                height={80}
                interval={0}
                tick={{ fontSize: 10 }}
              />

              <YAxis />
              <Tooltip />

              <Bar dataKey="value" fill="#f97316" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}