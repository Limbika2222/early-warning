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

        setData(res.trend_data)

        onMetricsChange({
          signalIndex: res.metrics.signal_index,
          spikeCount: res.metrics.spike_count,
          riskLevel: res.metrics.risk_level,
        })
      } catch {
        console.log("Failed to load chart data")
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

          <Line
            type="monotone"
            dataKey="value"
            name="Signal"
            stroke="#10b981"
            strokeWidth={2}
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="ewma"
            name="EWMA"
            stroke="#7c3aed"
            strokeWidth={2}
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="ucl"
            name="UCL"
            stroke="#ef4444"
            strokeDasharray="5 5"
            dot={false}
          />

          {data.map((point, index) =>
            point.is_spike ? (
              <ReferenceDot
                key={index}
                x={point.date}
                y={point.value}
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