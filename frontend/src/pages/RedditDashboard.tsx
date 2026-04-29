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
  LineChart,
  Line,
} from "recharts"

// ---------------- TYPES ----------------

interface TimeSeriesItem {
  date: string
  symptom: string
  count: number
}

interface Alert {
  date: string
  symptom: string
  actual: number
  expected: number
  z_score: number
  type: string
  generated_at?: string
}

interface Post {
  id: string
  title: string
  text: string
  created_date: string
  subreddit: string
}

interface Metrics {
  signal_index: number
  active_symptoms: number
  alerts: number
  top_symptom: string
}

interface RedditResponse {
  time_series: TimeSeriesItem[]
  alerts: Alert[]
  alert_history?: Alert[]
  metrics: Metrics
  posts: Post[]
}

interface ChartData {
  name: string
  value: number
}

// 🔥 KEEP ORIGINAL TYPE (unchanged)
interface MultiLineDataItem {
  date: string
  fever?: number
  cough?: number
  fatigue?: number
  headache?: number
  chills?: number
}

// ---------------- COMPONENT ----------------

export default function RedditDashboard() {
  const [barData, setBarData] = useState<ChartData[]>([])
  const [lineData, setLineData] = useState<MultiLineDataItem[]>([])
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [alertHistory, setAlertHistory] = useState<Alert[]>([])
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<string>("")
  const [selectedDate, setSelectedDate] = useState<string>("")

  const [cachedSeries, setCachedSeries] = useState<TimeSeriesItem[]>([])

  // ---------------- FETCH ----------------

  const fetchData = async () => {
    try {
      setLoading(true)

      const res = await fetch(
        `${import.meta.env.VITE_API_BASE}/api/reddit/signal`
      )

      const json: RedditResponse = await res.json()

      const baseSeries =
        cachedSeries.length > 0 ? cachedSeries : json.time_series

      if (cachedSeries.length === 0) {
        setCachedSeries(json.time_series)
      }

      const filteredSeries = selectedDate
        ? baseSeries.filter((d) => d.date === selectedDate)
        : baseSeries

      // ---------------- BAR ----------------
      const symptomCounts: Record<string, number> = {}

      filteredSeries.forEach((item) => {
        if (item.count > 0) {
          symptomCounts[item.symptom] =
            (symptomCounts[item.symptom] || 0) + item.count
        }
      })

      const formattedBar: ChartData[] = Object.entries(symptomCounts)
        .map(([symptom, count]) => ({
          name: symptom,
          value: count,
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 6)

      setBarData(formattedBar)

      // ---------------- MULTI-LINE (FIXED) ----------------
      const symptoms = ["fever", "cough", "fatigue", "headache", "chills"] as const
      type SymptomKey = typeof symptoms[number]

      const trendMap: Record<string, MultiLineDataItem> = {}

      filteredSeries.forEach((item) => {
        if (!trendMap[item.date]) {
          trendMap[item.date] = { date: item.date }
        }

        if (symptoms.includes(item.symptom as SymptomKey)) {
          const key = item.symptom as SymptomKey
          trendMap[item.date][key] = item.count
        }
      })

      setLineData(Object.values(trendMap))

      setMetrics(json.metrics)
      setAlerts(json.alerts)
      setAlertHistory(json.alert_history || [])
      setPosts(json.posts)

      setLastUpdated(new Date().toLocaleString())

    } catch (err) {
      console.error("❌ Reddit error:", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDate])

  // ---------------- UI ----------------

  return (
    <div className="bg-[#F1F5F9] min-h-screen p-6 space-y-6">

      {/* HEADER */}
      <div className="flex justify-between items-center flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-semibold">
            🧠 Reddit Health Intelligence
          </h1>
          <p className="text-xs text-gray-500 mt-1">
            Last updated: {lastUpdated || "—"}
          </p>
        </div>

        <div className="flex gap-2 items-center">
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="border px-2 py-1 rounded text-sm"
          />

          <button
            onClick={() => {
              setCachedSeries([])
              fetchData()
            }}
            className="bg-orange-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-orange-600"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* METRICS */}
      {metrics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card title="Signal Index" value={metrics.signal_index} />
          <Card title="Active Symptoms" value={metrics.active_symptoms} />
          <Card title="Alerts" value={metrics.alerts} highlight />
          <Card title="Top Symptom" value={metrics.top_symptom || "-"} />
        </div>
      )}

      {/* CHARTS */}
      <div className="grid md:grid-cols-2 gap-6">

        {/* LINE */}
        <div className="bg-white p-4 rounded-xl shadow-sm">
          <h2 className="text-sm mb-3 text-gray-600">
            📈 Symptom Trends
          </h2>

          {!loading && (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={lineData}>
                <CartesianGrid stroke="#eee" />

                <XAxis
                  dataKey="date"
                  angle={-35}
                  textAnchor="end"
                  height={70}
                  tick={{ fontSize: 10 }}
                />

                <YAxis />
                <Tooltip />

                <Line dataKey="fever" stroke="#ef4444" strokeWidth={2} />
                <Line dataKey="cough" stroke="#3b82f6" />
                <Line dataKey="fatigue" stroke="#22c55e" />
                <Line dataKey="headache" stroke="#f97316" />
                <Line dataKey="chills" stroke="#a855f7" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* BAR */}
        <div className="bg-white p-4 rounded-xl shadow-sm">
          <h2 className="text-sm mb-3 text-gray-600">
            📊 Symptom Ranking
          </h2>

          {!loading && (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={barData}>
                <CartesianGrid stroke="#eee" />
                <XAxis
                  dataKey="name"
                  angle={-25}
                  textAnchor="end"
                  height={70}
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

      {/* ALERTS */}
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <h2 className="text-sm mb-3 text-gray-600">🚨 Current Alerts</h2>

        {alerts.length === 0 ? (
          <p className="text-gray-400 text-sm">No alerts</p>
        ) : (
          alerts.map((a, i) => (
            <div key={i} className="bg-red-50 p-2 mb-2 text-sm border-l-4 border-red-500">
              {a.symptom.toUpperCase()} spike on {a.date} (z={a.z_score})
            </div>
          ))
        )}
      </div>

      {/* ALERT HISTORY */}
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <h2 className="text-sm mb-3 text-gray-600">📜 Alert History</h2>

        <div className="max-h-60 overflow-y-auto space-y-2">
          {alertHistory.map((a, i) => (
            <div key={i} className="border p-2 rounded text-sm">
              <p className="font-medium text-red-500">
                {a.symptom.toUpperCase()} spike
              </p>
              <p className="text-xs text-gray-500">Date: {a.date}</p>
              <p className="text-xs text-gray-400">
                Detected: {a.generated_at || "-"}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* POSTS */}
      <div className="bg-white p-4 rounded-xl shadow-sm">
        <h2 className="text-sm mb-3 text-gray-600">🧾 Reddit Posts</h2>

        {posts.map((p) => (
          <div key={p.id} className="border rounded-lg p-3 mb-2">
            <p className="font-semibold text-sm">{p.title}</p>
            <p className="text-xs text-gray-500">
              r/{p.subreddit} • {p.created_date}
            </p>
            <p className="text-sm text-gray-600">
              {p.text?.slice(0, 120)}
            </p>
          </div>
        ))}
      </div>

    </div>
  )
}

// ---------------- CARD ----------------

function Card({
  title,
  value,
  highlight = false,
}: {
  title: string
  value: number | string
  highlight?: boolean
}) {
  return (
    <div className="bg-white p-4 rounded-xl shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>
      <p className={`text-2xl font-semibold ${highlight ? "text-red-500" : ""}`}>
        {value}
      </p>
    </div>
  )
}