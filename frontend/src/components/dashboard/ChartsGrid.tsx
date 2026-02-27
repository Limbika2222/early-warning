import { useEffect, useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  ReferenceDot,
  Legend,
} from "recharts"

import { motion } from "framer-motion"
import ChartCard from "./ChartCard"
import { fetchSignalData } from "../../api/signal"

type DataSource = "google" | "twitter" | "who"

interface TrendPoint {
  date: string
  value: number
  ewma?: number
  ucl?: number
  is_spike?: boolean
}

interface Props {
  source: DataSource
  diseaseId: number
  countryId: number
  startDate?: string
  endDate?: string
  onMetricsChange?: (metrics: {
    signalIndex: number
    spikeCount: number
    riskLevel: string
  }) => void
}

const COLORS = ["#1f9c94", "#4f8ef7", "#7dd3fc"]

export default function ChartsGrid({
  source,
  diseaseId,
  countryId,
  startDate,
  endDate,
  onMetricsChange,
}: Props) {

  const [data, setData] = useState<TrendPoint[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [riskLevel, setRiskLevel] = useState<string>("Low")

  useEffect(() => {
    let cancelled = false

    async function loadData() {
      try {
        setLoading(true)

        const response = await fetchSignalData(
          source,
          diseaseId,
          countryId,
          startDate ?? "",
          endDate ?? ""
        )

        if (!cancelled) {
          const trend = response?.trend_data ?? []
          setData(trend)

          const risk = response?.metrics?.risk_level ?? "Low"
          setRiskLevel(risk)

          if (onMetricsChange && response?.metrics) {
            onMetricsChange({
              signalIndex: response.metrics.signal_index ?? 0,
              spikeCount: response.metrics.spike_count ?? 0,
              riskLevel: risk,
            })
          }

          setError(null)
        }
      } catch {
        if (!cancelled) {
          setError("No data available")
          setData([])
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadData()
    return () => { cancelled = true }
  }, [source, diseaseId, countryId, startDate, endDate, onMetricsChange])

  if (loading) return <div className="flex items-center justify-center h-48">Loading…</div>
  if (error) return <div className="text-red-500">{error}</div>
  if (!data.length) return <div>No data available</div>

  // ================= RISK COLOR LOGIC =================

  const riskColors: Record<string, string> = {
    Low: "rgba(34,197,94,0.08)",     // green
    Medium: "rgba(251,191,36,0.10)", // amber
    High: "rgba(239,68,68,0.10)",    // red
  }

  const overlayColor = riskColors[riskLevel] || "transparent"

  // ================= PIE DATA =================

  const pieData = [
    { name: "Low", value: data.filter(d => d.value < 40).length },
    { name: "Medium", value: data.filter(d => d.value >= 40 && d.value < 70).length },
    { name: "High", value: data.filter(d => d.value >= 70).length },
  ]

  // ================= WEEKLY DATA =================

  const weeklyMap: Record<number, { total: number; count: number }> = {}

  data.forEach((point, index) => {
    const week = Math.floor(index / 7)
    if (!weeklyMap[week]) weeklyMap[week] = { total: 0, count: 0 }
    weeklyMap[week].total += point.value
    weeklyMap[week].count += 1
  })

  const weeklyData = Object.entries(weeklyMap).map(([weekIndex, value]) => ({
    week: `W${Number(weekIndex) + 1}`,
    value: Math.round(value.total / value.count),
  }))

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{
        opacity: 1,
        backgroundColor: overlayColor,
      }}
      transition={{ duration: 0.6 }}
      className="space-y-8 p-4 rounded-2xl"
    >

      {/* ================= MAIN SURVEILLANCE CHART ================= */}

      <ChartCard title={`Disease Signal Surveillance (${source.toUpperCase()})`}>
        <ResponsiveContainer width="100%" height={340}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="date" hide />
            <YAxis />
            <Tooltip />
            <Legend />

            <Line
              type="monotone"
              dataKey="value"
              name="Signal"
              stroke="#1f9c94"
              strokeWidth={2.5}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="ewma"
              name="EWMA"
              stroke="#7c3aed"
              strokeWidth={2}
              strokeDasharray="6 4"
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="ucl"
              name="Control Limit"
              stroke="#ef4444"
              strokeWidth={1.5}
              strokeDasharray="3 3"
              dot={false}
            />

            {data.map((point, index) =>
              point.is_spike ? (
                <ReferenceDot
                  key={index}
                  x={point.date}
                  y={point.value}
                  r={6}
                  fill="#ef4444"
                  stroke="white"
                  strokeWidth={2}
                />
              ) : null
            )}
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* ================= LOWER GRID ================= */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <ChartCard title="Signal Intensity Distribution">
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                outerRadius={90}
                innerRadius={50}
                paddingAngle={4}
              >
                {pieData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Weekly Average Signal">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#cfe9e7" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Bar
                dataKey="value"
                fill="#4f8ef7"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

      </div>

    </motion.div>
  )
}