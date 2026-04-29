"use client"

import { useEffect, useState } from "react"
import Calendar from "react-calendar"
import "react-calendar/dist/Calendar.css"
import "../styles/calendar.css"

import DiseaseRankingBar from "../components/charts/DiseaseRankingBar"

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
  PieChart,
  Pie,
  Cell,
} from "recharts"

// ---------------- TYPES ----------------

type DataSource = "google" | "reddit" | "who"

interface ApiTrendPoint {
  date: string
  value?: number
  interest?: number
  symptom?: string
  is_spike?: boolean
}

interface RedditTimeSeries {
  date: string
  symptom: string
  count: number
}

interface RedditResponse {
  time_series: RedditTimeSeries[]
  metrics?: {
    signal_index: number
    alerts: number
  }
}

type DateRange = [Date, Date]

interface TrendData {
  date: string
  symptom: string
  interest: number
  is_spike: boolean
}

interface RankingItem {
  disease: string
  risk_score: number
}

interface TimeSeriesRow {
  date: string
  [key: string]: number | string
}

const COLORS = ["#6366F1", "#E5E7EB"]

// ---------------- DONUT ----------------
function Donut({
  value,
  max,
  label,
}: {
  value: number
  max: number
  label: string
}) {
  const percentage = Math.min((value / max) * 100, 100)

  return (
    <div className="bg-white p-4 rounded-2xl shadow-sm flex flex-col items-center">
      <ResponsiveContainer width={100} height={100}>
        <PieChart>
          <Pie
            data={[{ value: percentage }, { value: 100 - percentage }]}
            innerRadius={30}
            outerRadius={40}
            dataKey="value"
          >
            <Cell fill={COLORS[0]} />
            <Cell fill={COLORS[1]} />
          </Pie>
        </PieChart>
      </ResponsiveContainer>

      <p className="text-sm font-semibold mt-2">{label}</p>
      <p className="text-xs text-gray-500">{Math.round(value)}</p>
    </div>
  )
}

// ---------------- COMPONENT ----------------
export default function NewDashboard() {
  const [source, setSource] = useState<DataSource>("google")

  const [data, setData] = useState<TrendData[]>([])
  const [ranking, setRanking] = useState<{ name: string; value: number }[]>([])

  const [signalIndex, setSignalIndex] = useState(0)
  const [spikeCount, setSpikeCount] = useState(0)
  const [riskLevel, setRiskLevel] = useState("LOW")

  const [topSymptoms, setTopSymptoms] = useState<string[]>([])
  const [dateRange, setDateRange] = useState<DateRange | null>(null)

  const formatDate = (d: Date) => d.toISOString().split("T")[0]
  const handleReset = () => setDateRange(null)

  // -------------------------------------------------
  // LOAD DATA
  // -------------------------------------------------
  useEffect(() => {
    const load = async () => {
      try {
        const endDate = dateRange ? formatDate(dateRange[1]) : ""

        let url = ""

        if (source === "google") {
          url = `${import.meta.env.VITE_API_BASE}/api/signal?source=google&disease_id=1&country_id=1&end_date=${endDate}`
        }

        if (source === "reddit") {
          url = `${import.meta.env.VITE_API_BASE}/api/reddit/signal`
        }

        if (source === "who") {
          url = `${import.meta.env.VITE_API_BASE}/api/who`
        }

        const res = await fetch(url)
        const json = await res.json()

        let transformed: TrendData[] = []

        // ---------------- REDDIT ----------------
        if (source === "reddit") {
          const reddit: RedditResponse = json

          transformed = (reddit.time_series || []).map((d) => ({
            date: d.date,
            symptom: d.symptom,
            interest: d.count,
            is_spike: false,
          }))

          if (reddit.metrics) {
            setSignalIndex(reddit.metrics.signal_index)
            setSpikeCount(reddit.metrics.alerts)
            setRiskLevel("MEDIUM")
          }
        }

        // ---------------- GOOGLE / WHO ----------------
        else {
          transformed = (json.trend_data || []).map((d: ApiTrendPoint) => {
            const value = d.value ?? d.interest ?? 0

            return {
              date: d.date,
              interest: value,
              symptom: (d.symptom || "").toLowerCase().trim(),
              is_spike: d.is_spike ?? false,
            }
          })

          if (json.metrics) {
            setSignalIndex(json.metrics.signal_index)
            setSpikeCount(json.metrics.spike_count)
            setRiskLevel(json.metrics.risk_level)
          }
        }

        // FILTER
        transformed = transformed.filter(
          (d) =>
            d.symptom &&
            d.symptom !== "other" &&
            d.symptom.length > 2 &&
            d.interest >= 0
        )

        // DATE FILTER
        if (dateRange && source === "google") {
          const [start, end] = dateRange
          transformed = transformed.filter(
            (d) =>
              d.date >= formatDate(start) &&
              d.date <= formatDate(end)
          )
        }

        setData(transformed)

        // ---------------- TOP SYMPTOMS ----------------
        const totals: Record<string, number> = {}

        transformed.forEach((d) => {
          totals[d.symptom] = (totals[d.symptom] || 0) + d.interest
        })

        const top = Object.entries(totals)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5)
          .map(([k]) => k)

        setTopSymptoms(top)

        // ---------------- RANKING ----------------
        if (source === "google") {
          const rankingRes = await fetch(
            `${import.meta.env.VITE_API_BASE}/api/ranking/diseases?end_date=${endDate}`
          )

          const rankingData: RankingItem[] = await rankingRes.json()

          setRanking(
            rankingData.map((r) => ({
              name: r.disease,
              value: r.risk_score,
            }))
          )
        } else {
          setRanking([])
        }

      } catch (err) {
        console.error("🔥 LOAD ERROR:", err)
      }
    }

    load()
  }, [dateRange, source])

  // ---------------- TIME SERIES ----------------
  const symptomTimeSeries: TimeSeriesRow[] = Object.values(
    data.reduce<Record<string, TimeSeriesRow>>((acc, row) => {
      if (!acc[row.date]) acc[row.date] = { date: row.date }

      if (topSymptoms.includes(row.symptom)) {
        acc[row.date][row.symptom] = row.interest
      }

      return acc
    }, {})
  )

  // ---------------- DISTRIBUTION ----------------
  const symptomAgg = Object.values(
    data.reduce<Record<string, { name: string; value: number }>>(
      (acc, row) => {
        if (!acc[row.symptom]) {
          acc[row.symptom] = { name: row.symptom, value: 0 }
        }
        acc[row.symptom].value += row.interest
        return acc
      },
      {}
    )
  )

  const riskMap: Record<string, number> = {
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3,
  }

  const riskValue = riskMap[riskLevel] || 1

  return (
    <div className="bg-[#F8FAFC] min-h-screen p-6 grid grid-cols-12 gap-6">

      {/* LEFT */}
      <div className="col-span-12 lg:col-span-9 space-y-6">

        <h1 className="text-xl font-semibold">Infodemiology Dashboard</h1>

        {/* SOURCE SWITCH */}
        <div className="flex gap-2 bg-white p-1 rounded-xl shadow-sm w-fit">
          {["google", "reddit", "who"].map((s) => (
            <button
              key={s}
              onClick={() => setSource(s as DataSource)}
              className={`px-4 py-2 rounded-lg ${
                source === s
                  ? "bg-indigo-600 text-white"
                  : "text-gray-500 hover:bg-gray-100"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {/* METRICS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Donut label="Signal" value={signalIndex} max={5} />
          <Donut label="Spikes" value={spikeCount} max={10} />
          <Donut label="Risk" value={riskValue} max={3} />
          <Donut label="Data" value={data.length} max={5000} />
        </div>

        {/* RANKING */}
        {source === "google" && <DiseaseRankingBar data={ranking} />}

        {/* CHARTS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          {/* TIME SERIES */}
          <div className="bg-white p-4 rounded-2xl">
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={symptomTimeSeries}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                {topSymptoms.map((s) => (
                  <Area key={s} type="monotone" dataKey={s} />
                ))}
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* DISTRIBUTION */}
          <div className="bg-white p-4 rounded-2xl">
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={symptomAgg}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#6366F1" />
              </BarChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>

      {/* RIGHT */}
      <div className="col-span-12 lg:col-span-3 bg-white p-4 rounded-2xl space-y-3">
        <Calendar
          selectRange
          onChange={(v) => setDateRange(v as DateRange)}
          value={dateRange || undefined}
        />

        <button
          onClick={handleReset}
          className="w-full bg-gray-200 py-2 rounded-xl text-sm"
        >
          Reset
        </button>
      </div>
    </div>
  )
}