"use client"

import { useEffect, useState, useMemo } from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
} from "recharts"

// -------------------------------------------------
// TYPES
// -------------------------------------------------
interface DataItem {
  name: string
  value: number
  rank?: number
}

interface Props {
  data: DataItem[]
}

interface BarShapeProps {
  x?: number
  y?: number
  width?: number
  height?: number
  index?: number
}

// -------------------------------------------------
// COMPONENT
// -------------------------------------------------
export default function DiseaseRankingBar({ data }: Props) {
  const [animatedData, setAnimatedData] = useState<DataItem[]>([])

  // -------------------------------------------------
  // 🔥 SORT + RANK (MEMOIZED)
  // -------------------------------------------------
  const rankedData = useMemo(() => {
    return [...data]
      .sort((a, b) => b.value - a.value)
      .map((item, index) => ({
        ...item,
        rank: index + 1,
      }))
  }, [data])

  // -------------------------------------------------
  // 🔥 ANIMATION
  // -------------------------------------------------
  useEffect(() => {
    if (!rankedData.length) {
      setAnimatedData([])
      return
    }

    let frame = 0
    const duration = 15

    const interval = setInterval(() => {
      frame++
      const progress = frame / duration

      const newData = rankedData.map((item) => ({
        ...item,
        value: item.value * progress,
      }))

      setAnimatedData(newData)

      if (frame >= duration) {
        clearInterval(interval)
        setAnimatedData(rankedData)
      }
    }, 16)

    return () => clearInterval(interval)
  }, [rankedData])

  // -------------------------------------------------
  // UI
  // -------------------------------------------------
  return (
    <div className="bg-white p-3 rounded-xl shadow-sm">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-[11px] text-gray-500 font-medium">
          Disease Ranking
        </h2>
      </div>

      {animatedData.length === 0 ? (
        <p className="text-gray-400 text-xs">No ranking data</p>
      ) : (
        <ResponsiveContainer width="100%" height={200}>
          <BarChart
            data={animatedData}
            layout="vertical"
            margin={{ top: 0, right: 5, left: 0, bottom: 0 }}
            barCategoryGap={6}
          >
            <CartesianGrid
              stroke="#F9FAFB"
              horizontal={false}
              vertical={false}
            />

            <XAxis type="number" hide />

            <YAxis
              dataKey="name"
              type="category"
              width={100}
              tick={{ fontSize: 10, fill: "#6B7280" }}
              axisLine={false}
              tickLine={false}
            />

            <Tooltip />

            {/* MAIN BAR */}
            <Bar
              dataKey="value"
              radius={[0, 6, 6, 0]}
              barSize={10}
              animationDuration={400}
            >
              {animatedData.map((_, index) => (
                <Cell key={`cell-${index}`} fill="#6366F1" />
              ))}
            </Bar>

            {/* RANK LABEL */}
            <Bar
              dataKey="value"
              barSize={10}
              shape={(props: BarShapeProps) => {
                const {
                  x = 0,
                  y = 0,
                  width = 0,
                  height = 0,
                  index = 0,
                } = props

                const rank = animatedData[index]?.rank

                return (
                  <g>
                    <rect
                      x={x}
                      y={y}
                      width={width}
                      height={height}
                      rx={6}
                      fill="#6366F1"
                    />
                    <text
                      x={x - 6}
                      y={y + height / 2 + 3}
                      fontSize={9}
                      textAnchor="end"
                      fill="#9CA3AF"
                    >
                      {rank}
                    </text>
                  </g>
                )
              }}
            />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}