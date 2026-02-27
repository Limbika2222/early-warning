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

const COLORS = ["#22c55e", "#f59e0b", "#ef4444"]

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

          const risk = response?.risk_level ?? response?.metrics?.risk_level ?? "Low"
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
        if (!cancelled) setLoading(false)
      }
    }

    loadData()
    return () => { cancelled = true }
  }, [source, diseaseId, countryId, startDate, endDate, onMetricsChange])

  if (loading)
    return <div className="flex items-center justify-center h-48">Loading…</div>

  if (error)
    return <div className="text-red-500">{error}</div>

  if (!data.length)
    return <div>No data available</div>

  // ================= RISK BACKGROUND =================

  const riskColors: Record<string, string> = {
    Low: "rgba(34,197,94,0.08)",
    Medium: "rgba(245,158,11,0.10)",
    High: "rgba(239,68,68,0.12)",
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
      animate={{ opacity: 1, backgroundColor: overlayColor }}
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

            {/* Raw Signal */}
            <Line
              type="monotone"
              dataKey="value"
              name="Signal"
              stroke="#0ea5e9"
              strokeWidth={2.5}
              dot={false}
              animationDuration={800}
            />

            {/* EWMA */}
            <Line
              type="monotone"
              dataKey="ewma"
              name="EWMA"
              stroke="#7c3aed"
              strokeWidth={2}
              strokeDasharray="6 4"
              dot={false}
              animationDuration={1000}
            />

            {/* UCL */}
            <Line
              type="monotone"
              dataKey="ucl"
              name="Control Limit"
              stroke="#ef4444"
              strokeWidth={1.5}
              strokeDasharray="3 3"
              dot={false}
              animationDuration={1000}
            />

            {/* Spike Markers */}
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

        {/* Animated Pie */}
        <ChartCard title="Signal Intensity Distribution">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  outerRadius={95}
                  innerRadius={55}
                  paddingAngle={4}
                  isAnimationActive
                  animationDuration={900}
                  animationEasing="ease-out"
                  activeOuterRadius={105}
                >
                  {pieData.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>
        </ChartCard>

        {/* Weekly Bar */}
        <ChartCard title="Weekly Average Signal">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Bar
                dataKey="value"
                fill="#3b82f6"
                radius={[8, 8, 0, 0]}
                animationDuration={800}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

      </div>
    </motion.div>
  )
}