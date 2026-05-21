import { useEffect, useState } from "react"

import {
  AlertTriangle,
  Activity,
  Globe,
  Brain,
  Calendar,
} from "lucide-react"

import {
  fetchPredictions,
  fetchSeasonality,
  type Prediction,
} from "../api/predictions"

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts"

// =====================================================
// TYPES
// =====================================================

interface SeasonalityResult {
  disease: string
  peak_month: string
  top_months: string[]
  seasonality_strength: number
  seasonal_risk: string
}

// =====================================================
// COLORS
// =====================================================

function getRiskColor(risk: string) {
  if (risk === "HIGH") {
    return "bg-red-100 text-red-700"
  }

  if (risk === "MEDIUM") {
    return "bg-yellow-100 text-yellow-700"
  }

  return "bg-green-100 text-green-700"
}

// =====================================================
// COUNTRY MAP
// =====================================================

function getCountryName(code: string) {

  const countries: Record<string, string> = {
    ZA: "South Africa",
    US: "United States",
    IN: "India",
    GB: "United Kingdom",
    UG: "Uganda",
    CG: "Congo",
    CD: "DR Congo",
    RU: "Russia",
    DE: "Germany",
    MW: "Malawi",
    TZ: "Tanzania",
    KE: "Kenya",
    ET: "Ethiopia",
    NG: "Nigeria",
    GLOBAL: "Global",
  }

  return countries[code] || code
}

const COUNTRY_OPTIONS = [
  { code: "GLOBAL", name: "Global" },
  { code: "ZA", name: "South Africa" },
  { code: "IN", name: "India" },
  { code: "MW", name: "Malawi" },
  { code: "US", name: "United States" },
  { code: "NG", name: "Nigeria" },
  { code: "KE", name: "Kenya" },
  { code: "TZ", name: "Tanzania" },
  { code: "ET", name: "Ethiopia" },
]

// =====================================================
// COMPONENT
// =====================================================

export default function PredictionsDashboard() {

  const [predictions, setPredictions] =
    useState<Prediction[]>([])

  const [seasonality, setSeasonality] =
    useState<SeasonalityResult[]>([])

  const [loading, setLoading] =
    useState(true)

  const [selectedCountry, setSelectedCountry] =
    useState("GLOBAL")

  // ===================================================
  // FETCH DATA
  // ===================================================

  useEffect(() => {

    async function loadData() {

      setLoading(true)

      try {

        const predictionData =
          await fetchPredictions(
            selectedCountry
          )

        setPredictions(
          predictionData.predictions || []
        )

        const seasonalData =
          await fetchSeasonality(
            selectedCountry
          )

        setSeasonality(
          seasonalData.results || []
        )

      } catch (error) {

        console.error(error)

      } finally {

        setLoading(false)
      }
    }

    loadData()

  }, [selectedCountry])

  // ===================================================
  // STATS
  // ===================================================

  const highRiskCount =
    predictions.filter(
      (p) => p.risk_level === "HIGH"
    ).length

  const countries =
    new Set(
      predictions.map(
        (p) => p.country
      )
    ).size

  // ===================================================
  // CHART DATA
  // ===================================================

  const chartData =
    predictions.map((item) => ({
      disease: item.disease,
      score: item.combined_score,
    }))

  const strongSeasonality =
    seasonality.filter(

      (item) =>

        item.seasonality_strength >= 0.75
    )

  // ===================================================
  // LOADING
  // ===================================================

  if (loading) {

    return (
      <div className="p-6">
        <div className="text-gray-500">
          Loading prediction intelligence...
        </div>
      </div>
    )
  }

  if (
    !loading &&
    predictions.length === 0
  ) {
    return (
      <div className="p-6">

        <div
          className="
            bg-white
            border
            rounded-2xl
            p-10
            text-center
          "
        >

          <h2
            className="
              text-xl
              font-bold
              text-gray-700
            "
          >
            No intelligence available
          </h2>

          <p
            className="
              text-sm
              text-gray-500
              mt-2
            "
          >
            No outbreak signals detected for{" "}
            {getCountryName(
              selectedCountry
            )}
          </p>

        </div>

      </div>
    )
  }

  // ===================================================
  // UI
  // ===================================================

  return (

    <div className="p-6 space-y-6">

      {/* HEADER */}

      <div>
        <h1
          className="
            text-3xl
            font-bold
            text-gray-800
          "
        >
          AI Prediction Intelligence
        </h1>

        <p
          className="
            text-sm
            text-gray-500
            mt-1
          "
        >
          Multi-source outbreak forecasting for{" "}
          <strong>
            {getCountryName(selectedCountry)}
          </strong>
        </p>
      </div>

      {/* STATS */}

<div
  className="
    grid
    grid-cols-1
    md:grid-cols-2
    xl:grid-cols-4
    gap-4
  "
>

  {/* DISEASES */}

  <div
    className="
      bg-gradient-to-br
      from-indigo-500
      to-indigo-700
      text-white
      rounded-2xl
      p-5
      shadow-lg
    "
  >

    <div
      className="
        flex
        justify-between
        items-start
      "
    >

      <div>

        <p className="text-xs text-white/80">
          Diseases Predicted
        </p>

        <h2
          className="
            text-4xl
            font-bold
            mt-2
          "
        >
          {predictions.length}
        </h2>

      </div>

      <Brain
        size={30}
        className="text-white/80"
      />

    </div>

    {/* TAGS */}

    <div
      className="
        flex
        flex-wrap
        gap-2
        mt-5
      "
    >

      {predictions.map((item, index) => (

        <div
          key={index}
          className="
            px-2
            py-1
            rounded-full
            bg-white/20
            backdrop-blur-sm
            text-[11px]
            font-medium
          "
        >
          {item.disease}
        </div>

      ))}

    </div>

  </div>

  {/* HIGH RISK */}

  <div
    className="
      bg-gradient-to-br
      from-red-500
      to-red-700
      text-white
      rounded-2xl
      p-5
      shadow-lg
    "
  >

    <div
      className="
        flex
        justify-between
        items-center
      "
    >

      <div>

        <p className="text-xs text-white/80">
          High Risk
        </p>

        <h2
          className="
            text-4xl
            font-bold
            mt-2
          "
        >
          {highRiskCount}
        </h2>

      </div>

      <AlertTriangle
        size={30}
        className="text-white/80"
      />

    </div>

  </div>

  {/* COUNTRIES */}

  <div
    className="
      bg-gradient-to-br
      from-blue-500
      to-blue-700
      text-white
      rounded-2xl
      p-5
      shadow-lg
    "
  >

    <div
      className="
        flex
        justify-between
        items-center
      "
    >

      <div>

        <p className="text-xs text-white/80">
          Countries
        </p>

        <h2
          className="
            text-4xl
            font-bold
            mt-2
          "
        >
          {countries}
        </h2>

      </div>

      <Globe
        size={30}
        className="text-white/80"
      />

    </div>

  </div>

  {/* SOURCES */}

  <div
    className="
      bg-gradient-to-br
      from-emerald-500
      to-emerald-700
      text-white
      rounded-2xl
      p-5
      shadow-lg
    "
  >

    <div
      className="
        flex
        justify-between
        items-center
      "
    >

      <div>

        <p className="text-xs text-white/80">
          Sources
        </p>

        <h2
          className="
            text-4xl
            font-bold
            mt-2
          "
        >
          3
        </h2>

      </div>

      <Activity
        size={30}
        className="text-white/80"
      />

    </div>

  </div>

</div>

      {/* CHART */}

      <div
        className="
          bg-white
          border
          rounded-2xl
          p-5
          shadow-sm
        "
      >

        <div className="mb-4">

          <h2
            className="
              text-xl
              font-bold
              text-gray-800
            "
          >
            Disease Risk Intelligence
          </h2>

          <p
            className="
              text-sm
              text-gray-500
              mt-1
            "
          >
            Combined outbreak intelligence
          </p>

        </div>

        <div className="h-[220px]">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <AreaChart
              data={chartData}
            >

              <defs>

                <linearGradient
                  id="colorScore"
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >

                  <stop
                    offset="0%"
                    stopColor="#4f46e5"
                    stopOpacity={0.3}
                  />

                  <stop
                    offset="100%"
                    stopColor="#4f46e5"
                    stopOpacity={0.02}
                  />

                </linearGradient>

              </defs>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="disease"
                tick={{ fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                tick={{ fontSize: 10 }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip />

              <Area
                type="monotone"
                dataKey="score"
                stroke="#4f46e5"
                strokeWidth={2}
                fill="url(#colorScore)"
              />

            </AreaChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* SEASONAL FORECAST */}

<div
  className="
    bg-white
    border
    rounded-2xl
    p-5
    shadow-sm
  "
>

  <div
    className="
      flex
      items-center
      justify-between
      mb-5
    "
  >

    <div
      className="
        flex
        items-center
        gap-2
      "
    >

      <Calendar
        size={18}
        className="text-indigo-600"
      />

      <div>

        <h2
          className="
            text-lg
            font-bold
            text-gray-800
          "
        >
          Seasonal Forecast Intelligence
        </h2>

        <p
          className="
            text-xs
            text-gray-500
            mt-1
          "
        >
          Country-aware outbreak seasonality prediction
        </p>

      </div>

    </div>

    <div
      className="
        flex
        items-center
        gap-3
      "
    >

      <div
        className="
          text-xs
          uppercase
          tracking-wide
          text-gray-400
          font-semibold
        "
      >
        Intelligence Region
      </div>

      <select
        value={selectedCountry}
        onChange={(e) =>
          setSelectedCountry(
            e.target.value
          )
        }
        className="
          border
          rounded-xl
          px-4
          py-2
          text-sm
          bg-white
          shadow-sm
          focus:outline-none
          focus:ring-2
          focus:ring-indigo-500
        "
      >

        {COUNTRY_OPTIONS.map((country) => (

          <option
            key={country.code}
            value={country.code}
          >
            {country.name}
          </option>

        ))}

      </select>

    </div>

  </div>

  {strongSeasonality.length === 0 && (

    <div
      className="
        border
        rounded-2xl
        p-8
        text-center
        bg-slate-50
      "
    >

      <h3
        className="
          text-lg
          font-bold
          text-gray-700
        "
      >
        No Strong Seasonal Signals
      </h3>

      <p
        className="
          text-sm
          text-gray-500
          mt-2
        "
      >
        No high-confidence seasonal outbreak
        intelligence detected for this country.
      </p>

    </div>

  )}

  <div
    className="
      grid
      grid-cols-1
      lg:grid-cols-3
      gap-4
    "
  >

    {strongSeasonality.map((item) => (

      <div
        key={item.disease}
        className="
          relative
          overflow-hidden
          border
          rounded-2xl
          bg-gradient-to-br
          from-slate-50
          to-white
          p-5
        "
      >

        {/* TOP */}

        <div
          className="
            flex
            justify-between
            items-start
          "
        >

          <div>

            <h3
              className="
                text-xl
                font-bold
                text-gray-800
              "
            >
              {item.disease}
            </h3>

            <p
              className="
                text-xs
                text-gray-500
                mt-1
              "
            >
              {getCountryName(selectedCountry)}
              Seasonal Intelligence
            </p>

          </div>

          <div
            className={`
              px-2 py-1
              rounded-full
              text-[10px]
              font-semibold
              ${getRiskColor(item.seasonal_risk)}
            `}
          >
            {item.seasonal_risk}
          </div>

        </div>

        {/* PEAK */}

        <div className="mt-5">

          <p
            className="
              text-xs
              text-gray-500
            "
          >
            Peak Outbreak Month
          </p>

          <h4
            className="
              text-3xl
              font-bold
              text-indigo-600
              mt-1
            "
          >
            {item.peak_month}
          </h4>

        </div>

        {/* STRENGTH */}

        <div className="mt-5">

          <div
            className="
              flex
              justify-between
              items-center
              mb-2
            "
          >

            <p
              className="
                text-xs
                text-gray-500
              "
            >
              Seasonality Strength
            </p>

            <span
              className="
                text-sm
                font-bold
                text-gray-800
              "
            >
              {Math.round(
                item.seasonality_strength * 100
              )}%
            </span>

          </div>

          {/* PROGRESS BAR */}

          <div
            className="
              w-full
              h-2
              rounded-full
              bg-slate-200
              overflow-hidden
            "
          >

            <div
              className={`
                h-full
                rounded-full

                ${
                  item.seasonality_strength > 0.75

                  ? "bg-red-500"

                  : item.seasonality_strength > 0.5

                  ? "bg-yellow-500"

                  : "bg-green-500"
                }
              `}
              style={{
                width: `${
                  item.seasonality_strength * 100
                }%`,
              }}
            />

          </div>

        </div>

        {/* MONTHS */}

        <div className="mt-5">

          <p
            className="
              text-xs
              text-gray-500
              mb-2
            "
          >
            High Activity Months
          </p>

          <div
            className="
              flex
              flex-wrap
              gap-2
            "
          >

            {item.top_months.map((month) => (

              <div
                key={month}
                className="
                  px-3 py-1
                  rounded-full
                  bg-indigo-100
                  text-indigo-700
                  text-xs
                  font-medium
                "
              >
                {month}
              </div>

            ))}

          </div>

        </div>

        {/* FUTURE FEATURE */}

        <div
          className="
            mt-5
            pt-4
            border-t
            text-[11px]
            text-gray-400
          "
        >
          Country-level forecasting engine enabled
        </div>

      </div>

    ))}

  </div>

</div>

      {/* PREDICTION CARDS */}

      <div
        className="
          grid
          grid-cols-1
          lg:grid-cols-2
          gap-4
        "
      >

        {predictions.map((prediction, index) => (

          <div
            key={`${prediction.disease}-${index}`}
            className={`
              rounded-2xl
              p-5
              shadow-sm
              border

              ${
                prediction.risk_level === "HIGH"

                ? "bg-red-50 border-red-100"

                : prediction.risk_level === "MEDIUM"

                ? "bg-yellow-50 border-yellow-100"

                : "bg-green-50 border-green-100"
              }
            `}
          >

            <div
              className="
                flex
                justify-between
                items-start
              "
            >

              <div>

                <h2
                  className={`
                    text-2xl
                    font-bold

                    ${
                      prediction.risk_level === "HIGH"

                      ? "text-red-700"

                      : prediction.risk_level === "MEDIUM"

                      ? "text-yellow-700"

                      : "text-green-700"
                    }
                  `}
                >
                  {prediction.disease}
                </h2>

                <p
                  className="
                    text-sm
                    text-gray-500
                    mt-1
                  "
                >
                  Country:{" "}
                  {
                    getCountryName(
                      prediction.country
                    )
                  }
                </p>

              </div>

              <div
                className={`
                  px-3 py-1
                  rounded-full
                  text-xs
                  font-semibold
                  ${getRiskColor(
                    prediction.risk_level
                  )}
                `}
              >
                {prediction.risk_level}
              </div>

            </div>

            <div className="mt-5">

              <p
                className="
                  text-sm
                  text-gray-500
                "
              >
                Combined Score
              </p>

              <h3
                className="
                  text-4xl
                  font-bold
                  mt-1
                "
              >
                {prediction.combined_score}
              </h3>

            </div>

          </div>

        ))}

      </div>

    </div>
  )
}
