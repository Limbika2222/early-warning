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

interface Props {
  keywordId: number
  countryId: number
}

export default function ChartsGrid({ keywordId, countryId }: Props) {
  const [data, setData] = useState<TrendPoint[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    fetchInterestOverTime(keywordId, countryId)
      .then(result => {
        if (!cancelled) {
          setData(result)
          setError(null)
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError("No Google Trends data uploaded for this disease yet")
          setData([])
        }
      })

    return () => {
      cancelled = true
    }
  }, [keywordId, countryId])

  if (error) {
    return (
      <div className="text-red-600 text-center py-10">
        {error}
      </div>
    )
  }

  if (!data.length) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        No data available
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-6">
      <ChartCard title="Google Trends – Interest Over Time">
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
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  )
}
