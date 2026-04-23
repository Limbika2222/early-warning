"use client"

import { useEffect, useState } from "react"
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts"

interface DataPoint {
  date: string
  cases: number
}

export default function WhoDashboard() {
  const [data, setData] = useState<DataPoint[]>([])
  const [loading, setLoading] = useState(true)

  // ---------------- LOAD DATA ----------------
  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(
          "https://disease.sh/v3/covid-19/historical/all?lastdays=30"
        )
        const json = await res.json()

        const cases = json.cases || {}

        const formatted: DataPoint[] = Object.entries(cases).map(
          ([date, value]) => ({
            date,
            cases: value as number,
          })
        )

        setData(formatted)
      } catch (err) {
        console.error("WHO API ERROR:", err)
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  // ---------------- METRICS ----------------
  const latest = data[data.length - 1]?.cases || 0
  const previous = data[data.length - 2]?.cases || 0
  const growth = latest - previous

  if (loading) {
    return <div className="p-6">Loading WHO data...</div>
  }

  return (
    <div className="bg-[#F8FAFC] min-h-screen p-6 grid grid-cols-12 gap-6">

      {/* MAIN CONTENT AREA (MATCHES GOOGLE DASHBOARD) */}
      <div className="col-span-12 lg:col-span-9 space-y-6">

        <h1 className="text-xl font-semibold text-gray-800">
          WHO Disease Surveillance Dashboard
        </h1>

        {/* METRICS */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <MetricCard title="Total Cases" value={latest} />
          <MetricCard title="Daily Growth" value={growth} />
          <MetricCard title="Days" value={data.length} />
        </div>

        {/* CHARTS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          {/* AREA */}
          <div className="bg-white p-4 rounded-2xl shadow-sm">
            <h2 className="text-sm mb-2 text-gray-600">
              Cases Over Time
            </h2>

            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={data}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="cases"
                  stroke="#6366F1"
                  fill="#6366F1"
                  fillOpacity={0.15}
                  isAnimationActive
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* BAR */}
          <div className="bg-white p-4 rounded-2xl shadow-sm">
            <h2 className="text-sm mb-2 text-gray-600">
              Daily Cases
            </h2>

            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar
                  dataKey="cases"
                  fill="#10B981"
                  radius={[6, 6, 0, 0]}
                  isAnimationActive
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>

      {/* RIGHT PANEL (OPTIONAL - MATCH GOOGLE STYLE) */}
      <div className="col-span-12 lg:col-span-3 bg-white p-4 rounded-2xl shadow-sm">
        <h2 className="text-sm text-gray-600 mb-2">
          WHO Insights
        </h2>

        <p className="text-xs text-gray-500">
          Data source: disease.sh API
        </p>

        <p className="text-xs mt-2 text-gray-400">
          This dashboard shows real-time global disease trends.
        </p>
      </div>

    </div>
  )
}

// ---------------- METRIC CARD ----------------
function MetricCard({ title, value }: { title: string; value: number }) {
  return (
    <div className="bg-white p-4 rounded-2xl shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="text-xl font-semibold text-gray-800">
        {value.toLocaleString()}
      </p>
    </div>
  )
}