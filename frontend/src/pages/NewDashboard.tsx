"use client"

import { useEffect, useState, useCallback } from "react"
import Calendar from "react-calendar"
import "react-calendar/dist/Calendar.css"
import "../styles/calendar.css"

import { fetchSignalData, runAnalysis } from "../api/signal"
import MetricCard from "../components/dashboard/MetricCard"
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
} from "recharts"

type DateRange = [Date, Date]

/* =========================
   TYPES
========================= */

interface TrendPoint {
  date: string
  value?: number
  interest?: number
  symptom?: string
  is_spike?: boolean
}

interface TrendData {
  date: string
  symptom: string
  interest: number
  is_spike: boolean
}

type TimeSeriesRow = {
  date: string
  [key: string]: string | number
}

/* =========================
   DISEASE MAP
========================= */

const diseaseMap: Record<string, string[]> = {
  fever: ["Malaria", "Flu", "COVID"],
  cough: ["Flu", "COVID"],
  fatigue: ["COVID"],
  headache: ["Malaria", "Dengue"],
}

/* ========================= */

export default function NewDashboard() {
  const [data, setData] = useState<TrendData[]>([])
  const [signalIndex, setSignalIndex] = useState(0)
  const [spikeCount, setSpikeCount] = useState(0)
  const [riskLevel, setRiskLevel] = useState("No Data")
  const [loading, setLoading] = useState(false)

  const [dateRange, setDateRange] = useState<DateRange | null>(null)

  const formatDate = (date: Date) =>
    date.toISOString().split("T")[0]

  /* =========================
     🔥 LOAD SIGNAL (REAL DATA)
  ========================== */

  const loadSignal = useCallback(async () => {
    try {
      setLoading(true)

      const res = await fetchSignalData("google", 1, 1)

      const raw: TrendPoint[] = res?.trend_data || []

      let transformed: TrendData[] = raw.map((d) => ({
        date: d.date,
        interest: d.interest ?? d.value ?? 0,
        symptom: (d.symptom ?? "unknown").toLowerCase(),
        is_spike: d.is_spike ?? false,
      }))

      // 🔥 Date filtering
      if (dateRange) {
        const [start, end] = dateRange
        transformed = transformed.filter(
          (d) =>
            d.date >= formatDate(start) &&
            d.date <= formatDate(end)
        )
      }

      setData(transformed)

      // 🔥 Safe metrics
      setSignalIndex(res?.metrics?.signal_index ?? 0)
      setSpikeCount(res?.metrics?.spike_count ?? 0)
      setRiskLevel(res?.metrics?.risk_level ?? "No Data")

    } catch (err) {
      console.error("Error loading signal:", err)
    } finally {
      setLoading(false)
    }
  }, [dateRange])

  /* =========================
     🔥 RUN ANALYSIS + REFRESH
  ========================== */

  const handleRunAnalysis = async () => {
    try {
      setLoading(true)
      await runAnalysis()
      await loadSignal() // 🔥 refresh after pipeline
    } catch (err) {
      console.error("Analysis failed:", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSignal()
  }, [loadSignal])

  /* =========================
     🔥 INTELLIGENCE LAYER
  ========================== */

  const symptomAgg = Object.values(
    data.reduce(
      (acc: Record<string, { name: string; value: number }>, row) => {
        const symptom = row.symptom

        if (!acc[symptom]) {
          acc[symptom] = { name: symptom, value: 0 }
        }

        acc[symptom].value += row.interest
        return acc
      },
      {}
    )
  )

  const diseaseScores = Object.entries(
    data.reduce((acc: Record<string, number>, row) => {
      const diseases = diseaseMap[row.symptom] || []

      diseases.forEach((disease) => {
        acc[disease] = (acc[disease] || 0) + row.interest
      })

      return acc
    }, {})
  )
    .map(([name, value]) => ({
      name,
      value,
      year: 2024, // 🔥 dynamic later if needed
    }))
    .sort((a, b) => b.value - a.value)

  const symptomTimeSeries: TimeSeriesRow[] = Object.values(
    data.reduce(
      (acc: Record<string, TimeSeriesRow>, row) => {
        const date = row.date

        if (!acc[date]) {
          acc[date] = { date }
        }

        acc[date][row.symptom] = row.interest

        return acc
      },
      {}
    )
  )

  /* =========================
     🔥 ILLNESS CLASSIFICATION
  ========================== */

  const illnessScores = data.reduce((acc: Record<string, number>, row) => {
    const symptom = row.symptom

    if (["fever", "cough", "fatigue"].includes(symptom)) {
      acc["respiratory"] = (acc["respiratory"] || 0) + row.interest
    }

    if (["anosmia", "loss_of_taste", "breathlessness"].includes(symptom)) {
      acc["covid"] = (acc["covid"] || 0) + row.interest
    }

    if (["headache"].includes(symptom)) {
      acc["general"] = (acc["general"] || 0) + row.interest
    }

    return acc
  }, {})

  function classifyIllness(scores: Record<string, number>) {
    const respiratory = scores["respiratory"] || 0
    const covid = scores["covid"] || 0

    if (covid > respiratory * 0.4 && covid > 20) {
      return {
        label: "COVID-like Illness",
        risk: "HIGH",
        color: "text-red-500",
      }
    }

    if (respiratory > 20) {
      return {
        label: "Influenza-like Illness",
        risk: "MEDIUM",
        color: "text-yellow-500",
      }
    }

    return {
      label: "General Infection",
      risk: "LOW",
      color: "text-green-500",
    }
  }

  const illness = classifyIllness(illnessScores)

  /* ========================= */

  return (
    <div className="bg-[#F8FAFC] min-h-screen p-6 grid grid-cols-12 gap-6">

      <div className="col-span-12 lg:col-span-9 space-y-6">

        <h1 className="text-xl font-semibold text-gray-800">
          Infodemiology Dashboard
        </h1>

        {/* METRICS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <MetricCard title="Signal" value={signalIndex.toFixed(2)} />
          <MetricCard title="Spikes" value={spikeCount} />
          <MetricCard title="Risk" value={riskLevel} />
          <MetricCard title="Data" value={data.length} />
        </div>

        {/* CLASSIFICATION */}
        <div className="bg-white p-4 rounded-2xl shadow-sm border-l-4 border-indigo-500">
          <h2 className="text-sm text-gray-500 mb-1">
            Illness Classification
          </h2>

          <p className={`text-lg font-semibold ${illness.color}`}>
            {illness.label}
          </p>

          <p className="text-xs text-gray-400 mt-1">
            Risk Level: {illness.risk}
          </p>
        </div>

        {/* 🔥 REAL DATA RANKING */}
        <DiseaseRankingBar data={diseaseScores} />

        {/* CHARTS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <div className="bg-white p-4 rounded-2xl shadow-sm">
            <h2 className="text-sm mb-2 text-gray-600">
              Top Symptoms Over Time
            </h2>

            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={symptomTimeSeries}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />

                <Area type="monotone" dataKey="fever" stroke="#6366F1" fillOpacity={0.15} />
                <Area type="monotone" dataKey="cough" stroke="#10B981" fillOpacity={0.15} />
                <Area type="monotone" dataKey="fatigue" stroke="#F59E0B" fillOpacity={0.15} />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white p-4 rounded-2xl shadow-sm">
            <h2 className="text-sm mb-2 text-gray-600">
              Symptom Distribution
            </h2>

            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={symptomAgg}>
                <CartesianGrid stroke="#E5E7EB" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#6366F1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>

      {/* CALENDAR */}
      <div className="col-span-12 lg:col-span-3 bg-white p-4 rounded-2xl shadow-sm">
        <Calendar
          selectRange
          onChange={(value) => setDateRange(value as DateRange)}
        />

        <button
          onClick={handleRunAnalysis}
          className="mt-4 w-full bg-[#6366F1] hover:bg-[#4F46E5] text-white py-2 rounded-xl"
        >
          {loading ? "Running..." : "Run Analysis"}
        </button>
      </div>

    </div>
  )
}