"use client"

import {
  useEffect,
  useMemo,
  useState,
} from "react"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
  LabelList,
} from "recharts"

// =====================================================
// TYPES
// =====================================================

interface DataItem {
  name: string
  value: number
  rank?: number
}

interface Props {
  data: DataItem[]
}

// =====================================================
// COMPONENT
// =====================================================

export default function DiseaseRankingBar({
  data,
}: Props) {

  const [animatedData, setAnimatedData] =
    useState<DataItem[]>([])

  // =====================================================
  // SORT + RANK
  // =====================================================

  const rankedData = useMemo(() => {

    return [...data]
      .sort((a, b) => b.value - a.value)
      .map((item, index) => ({
        ...item,
        rank: index + 1,
      }))

  }, [data])

  // =====================================================
  // ANIMATION
  // =====================================================

  useEffect(() => {

    setAnimatedData([])

    if (!rankedData.length) {
      return
    }

    let frame = 0

    const duration = 20

    const interval = setInterval(() => {

      frame++

      const progress =
        Math.min(frame / duration, 1)

      const next = rankedData.map(
        (item) => ({
          ...item,
          value:
            item.value * progress,
        })
      )

      setAnimatedData(next)

      if (progress >= 1) {

        clearInterval(interval)

        setAnimatedData(rankedData)
      }

    }, 16)

    return () => clearInterval(interval)

  }, [rankedData])

  // =====================================================
  // EMPTY STATE
  // =====================================================

  if (!animatedData.length) {

    return (
      <div className="bg-white p-3 rounded-xl shadow-sm">

        <div className="flex justify-between items-center mb-2">

          <h2 className="text-[11px] text-gray-500 font-medium">
            Disease Ranking
          </h2>

        </div>

        <p className="text-gray-400 text-xs">
          No ranking data
        </p>

      </div>
    )
  }

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="bg-white p-3 rounded-xl shadow-sm">

      <div className="flex justify-between items-center mb-2">

        <h2 className="text-[11px] text-gray-500 font-medium">
          Disease Ranking
        </h2>

      </div>

      <ResponsiveContainer
        width="100%"
        height={220}
      >

        <BarChart
          data={animatedData}
          layout="vertical"
          margin={{
            top: 0,
            right: 20,
            left: 10,
            bottom: 0,
          }}
          barCategoryGap={8}
        >

          <CartesianGrid
            stroke="#F3F4F6"
            horizontal={false}
            vertical={false}
          />

          <XAxis
            type="number"
            hide
          />

          <YAxis
            dataKey="name"
            type="category"
            width={110}
            tick={{
              fontSize: 10,
              fill: "#6B7280",
            }}
            axisLine={false}
            tickLine={false}
          />

          {/* ================================================= */}
          {/* TOOLTIP */}
          {/* ================================================= */}

          <Tooltip
            formatter={(value) => {

              const numericValue =
                typeof value === "number"
                  ? value
                  : Number(value) || 0

              return [
                numericValue.toFixed(2),
                "Risk Score",
              ]
            }}
          />

          {/* ================================================= */}
          {/* BAR */}
          {/* ================================================= */}

          <Bar
            dataKey="value"
            radius={[0, 6, 6, 0]}
            barSize={12}
            animationDuration={300}
          >

            {animatedData.map(
              (_, index) => (

                <Cell
                  key={`cell-${index}`}
                  fill="#6366F1"
                />

              )
            )}

            {/* VALUE LABEL */}

            <LabelList
              dataKey="value"
              position="right"
              formatter={(value) => {

                const numericValue =
                  typeof value === "number"
                    ? value
                    : Number(value) || 0

                return numericValue.toFixed(1)
              }}
              style={{
                fontSize: 10,
                fill: "#6B7280",
              }}
            />

            {/* RANK LABEL */}

            <LabelList
              dataKey="rank"
              position="left"
              offset={10}
              style={{
                fontSize: 9,
                fill: "#9CA3AF",
              }}
            />

          </Bar>

        </BarChart>

      </ResponsiveContainer>

    </div>
  )
}