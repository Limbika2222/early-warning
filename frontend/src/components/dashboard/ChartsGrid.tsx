import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

import ChartCard from "./ChartCard"
import { dashboardMockData } from "../../data/mockDashboardData"

export default function ChartsGrid() {
  return (
    <div className="grid grid-cols-2 gap-6">
      {/* Official Reported Cases */}
      <ChartCard title="Official Reported Cases">
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={dashboardMockData}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="cases"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              isAnimationActive
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Google Trends */}
      <ChartCard title="Google Trends – Symptom Search Interest">
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={dashboardMockData}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="trends"
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
