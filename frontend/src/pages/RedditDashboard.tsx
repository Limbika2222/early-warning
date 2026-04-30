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
  probable_diseases?: Disease[]
}

interface ChartData {
  name: string
  value: number
}

interface Disease {
  disease: string
  probability: number
}

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
  const [diseases, setDiseases] = useState<Disease[]>([])

  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<string>("")

  const [startDate, setStartDate] = useState<string>("")
  const [endDate, setEndDate] = useState<string>("")

  // ---------------- FETCH ----------------

  const fetchData = async () => {
    try {
      setLoading(true)

      const query = new URLSearchParams()

      if (startDate) query.append("start_date", startDate)
      if (endDate) query.append("end_date", endDate)

      const res = await fetch(
        `${import.meta.env.VITE_API_BASE}/api/reddit/signal?${query.toString()}`
      )

      const json: RedditResponse = await res.json()

      setDiseases(json.probable_diseases || [])

      const baseSeries = json.time_series

      const filteredSeries = baseSeries.filter((d) => {
        const current = new Date(d.date)

        if (startDate && current < new Date(startDate)) return false
        if (endDate && current > new Date(endDate)) return false

        return true
      })

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

      const rawData = Object.values(trendMap)

      const smoothData = rawData.map((point, index, arr) => {
        const getAvg = (key: keyof MultiLineDataItem) => {
          let sum = 0
          let count = 0

          for (let i = index - 1; i <= index + 1; i++) {
            if (arr[i] && typeof arr[i][key] === "number") {
              sum += arr[i][key] as number
              count++
            }
          }

          return count > 0 ? Math.round(sum / count) : 0
        }

        return {
          date: point.date,
          fever: getAvg("fever"),
          cough: getAvg("cough"),
          fatigue: getAvg("fatigue"),
          headache: getAvg("headache"),
          chills: getAvg("chills"),
        }
      })

      setLineData(smoothData)

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
    // eslint-disable-next-line
  }, [startDate, endDate])

  const symptomColors = {
    fever: "#EF4444",
    cough: "#F59E0B",
    fatigue: "#6366F1",
    headache: "#8B5CF6",
    chills: "#06B6D4",
  }

  return (
    <div className="bg-slate-50 min-h-screen p-6 space-y-6">

      {/* HEADER */}
      <div className="flex justify-between items-center flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-slate-800">
            🧠 Reddit Health Intelligence
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Last updated: {lastUpdated || "—"}
          </p>
        </div>

        <div className="flex gap-2 items-center">

          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
          />

          <span className="text-xs text-slate-400">to</span>

          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
          />

          <button
            onClick={() => {
              setStartDate("")
              setEndDate("")
              fetchData()
            }}
            className="bg-slate-200 text-slate-700 hover:bg-slate-300 px-3 py-1 rounded-md text-sm"
          >
            Reset
          </button>

          <button
            onClick={fetchData}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm"
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

        <div className="bg-white border border-gray-200 rounded-2xl p-4">
          <h2 className="text-sm mb-3 text-slate-500">📈 Symptom Trends</h2>

          {!loading && (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={lineData}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="date" angle={-35} textAnchor="end" height={70} tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Line dataKey="fever" stroke={symptomColors.fever} strokeWidth={2} dot={false} />
                <Line dataKey="cough" stroke={symptomColors.cough} dot={false} />
                <Line dataKey="fatigue" stroke={symptomColors.fatigue} dot={false} />
                <Line dataKey="headache" stroke={symptomColors.headache} dot={false} />
                <Line dataKey="chills" stroke={symptomColors.chills} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl p-4">
          <h2 className="text-sm mb-3 text-slate-500">📊 Symptom Ranking</h2>

          {!loading && (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={barData}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="name" angle={-25} textAnchor="end" height={70} tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#6366F1" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* DISEASES */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4">
        <h2 className="text-sm mb-4 text-slate-500">🧠 Probable Diseases</h2>
        {diseases.map((d, i) => (
          <div key={i} className="mb-2">
            <div className="flex justify-between text-sm text-slate-800 mb-1">
              <span>{d.disease}</span>
              <span>{(d.probability * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div
                className="h-2 bg-indigo-600 rounded-full"
                style={{ width: `${d.probability * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* ALERTS */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4">
        <h2 className="text-sm mb-3 text-slate-500">🚨 Current Alerts</h2>
        {alerts.length === 0 ? (
          <p className="text-slate-400 text-sm">No alerts</p>
        ) : (
          alerts.map((a, i) => (
            <div key={i} className="bg-red-50 border border-red-200 text-red-700 rounded-lg px-3 py-2 text-sm mb-2">
              {a.symptom.toUpperCase()} spike on {a.date}
            </div>
          ))
        )}
      </div>

      {/* ALERT HISTORY (RESTORED) */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4">
        <h2 className="text-sm mb-3 text-slate-500">📜 Alert History</h2>
        {alertHistory.length === 0 ? (
          <p className="text-slate-400 text-sm">No history</p>
        ) : (
          alertHistory.map((a, i) => (
            <div key={i} className="text-xs text-slate-500 border-b border-slate-200 py-1">
              [{a.generated_at}] {a.symptom} spike on {a.date}
            </div>
          ))
        )}
      </div>

      {/* POSTS */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4">
        <h2 className="text-sm mb-3 text-slate-500">🧾 Reddit Posts</h2>
        {posts.map((p) => (
          <div key={p.id} className="border border-gray-200 rounded-xl p-3 mb-2">
            <p className="font-semibold text-sm text-slate-800">{p.title}</p>
            <p className="text-xs text-slate-500">
              r/{p.subreddit} • {p.created_date}
            </p>
            <p className="text-sm text-slate-600">
              {p.text?.slice(0, 120)}...
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
    <div className="bg-white border border-gray-200 rounded-2xl p-4">
      <p className="text-sm text-slate-500">{title}</p>
      <p className={`text-2xl font-semibold ${highlight ? "text-red-500" : "text-slate-800"}`}>
        {value}
      </p>
    </div>
  )
}
