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
import { fetchAggregatedDiseaseSignal } from "../../api/trends"
import type { TrendPoint } from "../../api/trends"

interface Props {
  diseaseId: number
  countryId: number
  startDate: string // YYYY-MM-DD
  endDate: string   // YYYY-MM-DD
}

export default function ChartsGrid({
  diseaseId,
  countryId,
  startDate,
  endDate,
}: Props) {
  /**
   * data === null  -> loading
   * data.length   -> success
   * error !== null-> error
   */
  const [data, setData] = useState<TrendPoint[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    // Reset state whenever inputs change
    setData(null)
    setError(null)

    fetchAggregatedDiseaseSignal(
      diseaseId,
      countryId,
      startDate,
      endDate
    )
      .then(result => {
        if (!cancelled) {
          setData(result)
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError("No Google Trends data for selected range")
        }
      })

    return () => {
      cancelled = true
    }
  }, [diseaseId, countryId, startDate, endDate])

  // ---------------- UI STATES ----------------

  if (data === null && !error) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        Loading disease signal…
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

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        No data available for selected range
      </div>
    )
  }

  // ---------------- CHART ----------------

  return (
    <div className="grid grid-cols-1 gap-6">
      <ChartCard title="Aggregated Disease Signal (Google Trends)">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <XAxis dataKey="date" hide />
            <YAxis />
            <Tooltip
              labelFormatter={label =>
                typeof label === "string"
                  ? new Date(label).toLocaleDateString()
                  : ""
              }
            />
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
