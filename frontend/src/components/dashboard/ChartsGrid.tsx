import { useEffect, useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceDot,
  Legend,
} from "recharts"

import { fetchSignalData, type TrendPoint } from "../../api/signal"

interface Props {
  source: string
  diseaseId: number
  countryId: number
  startDate?: string
  endDate?: string
  onMetricsChange: (metrics: {
    signalIndex: number
    spikeCount: number
    riskLevel: string
  }) => void
}

export default function ChartsGrid({
  source,
  diseaseId,
  countryId,
  startDate,
  endDate,
  onMetricsChange,
}: Props) {
  const [data, setData] = useState<TrendPoint[]>([])

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await fetchSignalData(
          source,
          diseaseId,
          countryId,
          startDate,
          endDate
        )

        const raw = res.trend_data || []

        // ✅ SAFE TRANSFORM (NO TYPE ERROR)
        const withChange: TrendPoint[] = raw.map((d, i, arr) => {
          const current = d.interest ?? 0
          const prev = i > 0 ? arr[i - 1].interest ?? 0 : current

          return {
            ...d,
            interest: current,
            change: current - prev,
          }
        })

        setData(withChange)

        onMetricsChange({
          signalIndex: res.metrics.signal_index,
          spikeCount: res.metrics.spike_count,
          riskLevel: res.metrics.risk_level,
        })
      } catch (err) {
        console.error("Failed to load chart data", err)
      }
    }

    loadData()
  }, [source, diseaseId, countryId, startDate, endDate, onMetricsChange])

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" hide />
          <YAxis />
          <Tooltip />
          <Legend />

          {/* BASELINE */}
          <Line
            type="monotone"
            dataKey="interest"
            name="Interest"
            stroke="#94a3b8"
            strokeWidth={1}
            dot={false}
          />

          {/* 🔥 MAIN SIGNAL */}
          <Line
            type="monotone"
            dataKey="change"
            name="Change"
            stroke="#10b981"
            strokeWidth={3}
            dot={false}
          />

          {/* OPTIONAL */}
          <Line
            type="monotone"
            dataKey="ewma"
            name="EWMA"
            stroke="#7c3aed"
            strokeWidth={2}
            dot={false}
          />

          {/* SPIKES */}
          {data.map((point, index) =>
            point.is_spike ? (
              <ReferenceDot
                key={index}
                x={point.date}
                y={point.change ?? 0}
                r={5}
                fill="red"
              />
            ) : null
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}