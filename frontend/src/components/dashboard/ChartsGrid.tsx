import { useEffect, useState } from "react"
import {
  AreaChart,
  Area,
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
} from "recharts"

import { motion } from "framer-motion"
import ChartCard from "./ChartCard"
import { fetchSignalData } from "../../api/signal"

type DataSource = "google" | "twitter" | "who"

interface TrendPoint {
  date: string
  value: number
}

interface Props {
  source: DataSource
  diseaseId: number
  countryId: number
  startDate?: string   // ✅ optional now
  endDate?: string     // ✅ optional now
  onMetricsChange?: (metrics: {
    signalIndex: number
    spikeCount: number
    riskLevel: string
  }) => void
}

interface PieDataItem {
  name: string
  value: number
}

interface WeeklyDataItem {
  week: string
  value: number
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

  useEffect(() => {
    let cancelled = false

    async function loadData() {
      try {
        setLoading(true)

        const response = await fetchSignalData(
          source,
          diseaseId,
          countryId,
          startDate ?? "",   // ✅ safe fallback
          endDate ?? ""      // ✅ safe fallback
        )

        if (!cancelled) {
          const trend = response?.trend_data ?? []
          setData(trend)

          if (onMetricsChange && response?.metrics) {
            onMetricsChange({
              signalIndex: response.metrics.signal_index ?? 0,
              spikeCount: response.metrics.spike_count ?? 0,
              riskLevel: response.metrics.risk_level ?? "Unknown",
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

    return () => {
      cancelled = true
    }
  }, [source, diseaseId, countryId, startDate, endDate, onMetricsChange])

  // ================= STATES =================

  if (loading) {
    return (
      <div className="flex items-center justify-center h-48 text-[#1e3f42]">
        Loading charts…
      </div>
    )
  }

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  if (!data.length) {
    return <div className="text-[#3b6b6f]">No data available</div>
  }

  // ================= PIE DATA =================

  const pieData: PieDataItem[] = [
    { name: "Low", value: data.filter(d => d.value < 40).length },
    { name: "Medium", value: data.filter(d => d.value >= 40 && d.value < 70).length },
    { name: "High", value: data.filter(d => d.value >= 70).length },
  ]

  // ================= WEEKLY DATA =================

  const weeklyMap: Record<number, { total: number; count: number }> = {}

  data.forEach((point, index) => {
    const week = Math.floor(index / 7)

    if (!weeklyMap[week]) {
      weeklyMap[week] = { total: 0, count: 0 }
    }

    weeklyMap[week].total += point.value
    weeklyMap[week].count += 1
  })

  const weeklyData: WeeklyDataItem[] = Object.entries(weeklyMap).map(
    ([weekIndex, value]) => ({
      week: `W${Number(weekIndex) + 1}`,
      value: Math.round(value.total / value.count),
    })
  )

  // ================= UI =================

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-8"
    >
      {/* ================= MAIN AREA CHART ================= */}
      <ChartCard title={`Disease Signal Trend (${source.toUpperCase()})`}>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="signalGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#1f9c94" stopOpacity={0.35} />
                <stop offset="95%" stopColor="#1f9c94" stopOpacity={0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#cfe9e7" />

            <XAxis
              dataKey="date"
              stroke="#3b6b6f"
              tick={{ fill: "#3b6b6f", fontSize: 11 }}
              hide
            />

            <YAxis
              stroke="#3b6b6f"
              tick={{ fill: "#3b6b6f", fontSize: 11 }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                borderRadius: "12px",
                border: "1px solid #e2f3f2",
                color: "#1e3f42",
              }}
              cursor={{ stroke: "#1f9c94", strokeWidth: 1 }}
            />

            <Area
              type="monotone"
              dataKey="value"
              stroke="#1f9c94"
              strokeWidth={3}
              fill="url(#signalGradient)"
              dot={false}
              activeDot={{
                r: 6,
                stroke: "#1f9c94",
                strokeWidth: 2,
                fill: "white",
              }}
              animationDuration={800}
            />
          </AreaChart>
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
              <XAxis dataKey="week" stroke="#3b6b6f" />
              <YAxis stroke="#3b6b6f" />
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