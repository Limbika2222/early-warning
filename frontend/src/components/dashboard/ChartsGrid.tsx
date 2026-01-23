import { useEffect, useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

import ChartCard from "./ChartCard"
import { fetchInterestOverTime } from "../../api/trends"
import type { TrendPoint } from "../../api/trends"

export default function ChartsGrid() {
  const [data, setData] = useState<TrendPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchInterestOverTime(1, 1) // fever cough, India
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        Loading real epidemiological signals…
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-red-600 text-center py-10">
        {error}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-6">
      <ChartCard title="Google Trends – Fever & Cough (India)">
        <ResponsiveContainer height={300}>
          <LineChart data={data}>
            <XAxis dataKey="date" hide />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#0ea5e9"
              strokeWidth={2}
              dot={false}
              isAnimationActive
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  )
}
