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
  type SeasonalityResult,
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

const uniqueDiseases = [

  ...new Set(

    predictions.map(
      (p) => p.disease
    )
  )
]

const affectedCountries = [

  ...new Set(

    predictions.map(
      (p) => p.country
    )
  )
]

const highRiskDiseases = [

  ...new Set(

    predictions

      .filter(
        (p) =>
          p.risk_level === "HIGH"
      )

      .map(
        (p) => p.disease
      )
  )
]

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

  const consolidatedSeasonality =
    Object.values(

      strongSeasonality.reduce(

        (acc, item) => {

          const disease =
            item.disease

          // FIRST ENTRY

          if (!acc[disease]) {

            acc[disease] = {

              ...item,

              secondary_peaks: [],
            }

          }

          // ADD EXTRA PEAKS

          else {

            const existing =
              acc[disease]

            // STORE SECONDARY PEAK

            if (
              item.peak_month !==
              existing.peak_month
            ) {

              if (
                !existing.secondary_peaks.includes(
                  item.peak_month
                )
              ) {
                existing.secondary_peaks.push(
                  item.peak_month
                )
              }
            }

            // KEEP STRONGEST
            // AS PRIMARY

            if (
              item.seasonality_strength >
              existing.seasonality_strength
            ) {

              if (
                !existing.secondary_peaks.includes(
                  existing.peak_month
                )
              ) {
                existing.secondary_peaks.push(
                  existing.peak_month
                )
              }

              existing.peak_month =
                item.peak_month

              existing.seasonality_strength =
                item.seasonality_strength
            }
          }

          return acc

        },

        {} as Record<
          string,
          SeasonalityResult
        >
      )
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

      <div className="flex justify-between items-start">
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

      {uniqueDiseases.map((disease, index) => (

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
          {disease}
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

<div
  className="
    mt-5
    flex
    flex-wrap
    gap-2
  "
>

  {highRiskDiseases.map(
    (disease) => (

      <div
        key={disease}
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
        {disease}
      </div>

    )
  )}

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

<div
  className="
    mt-5
    flex
    flex-wrap
    gap-2
  "
>

  {affectedCountries.map(
    (country) => (

      <div
        key={country}
        className="
          px-2
          py-1
          rounded-full
          bg-white/20
          text-[11px]
          font-medium
        "
      >
        {
          getCountryName(
            country
          )
        }
      </div>

    )
  )}

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

<div
  className="
    mt-5
    space-y-2
    text-xs
  "
>

  <div
    className="
      flex
      items-center
      gap-2
    "
  >
    <div
      className="
        w-2
        h-2
        rounded-full
        bg-green-300
      "
    />
    Google Trends
  </div>

  <div
    className="
      flex
      items-center
      gap-2
    "
  >
    <div
      className="
        w-2
        h-2
        rounded-full
        bg-green-300
      "
    />
    WHO Surveillance
  </div>

  <div
    className="
      flex
      items-center
      gap-2
    "
  >
    <div
      className="
        w-2
        h-2
        rounded-full
        bg-green-300
      "
    />
    Reddit Signals
  </div>

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

    {consolidatedSeasonality.map((item) => (

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
            Primary Seasonal Peak
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

        {(() => {

  const cleanSecondaryPeaks =

    [...new Set(

      item.secondary_peaks.filter(

        (month) =>

          month !== item.peak_month
      )
    )]

  return (

    cleanSecondaryPeaks.length > 0 && (

      <div className="mt-3">

        <p
          className="
            text-xs
            text-gray-500
            mb-2
          "
        >
          Secondary Peaks
        </p>

        <div
          className="
            flex
            flex-wrap
            gap-2
          "
        >

          {cleanSecondaryPeaks.map(
            (month, index) => (

              <div
                key={`${month}-${index}`}
                className="
                  px-2
                  py-1
                  rounded-full
                  bg-orange-100
                  text-orange-700
                  text-xs
                  font-medium
                "
              >
                {month}
              </div>

            )
          )}

        </div>

      </div>

    )

  )

})()}

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
    relative
    rounded-2xl
    border
    p-4
    transition-all
    duration-200
    hover:shadow-md

    ${
      prediction.risk_level === "HIGH"

      ? "bg-red-50 border-red-100"

      : prediction.risk_level === "MEDIUM"

      ? "bg-yellow-50 border-yellow-100"

      : "bg-emerald-50 border-emerald-100"
    }
  `}
>

  {/* TOP ROW */}

  <div
    className="
      flex
      items-start
      justify-between
      gap-3
    "
  >

    <div>

      <h2
        className={`
          text-xl
          font-bold
          leading-none

          ${
            prediction.risk_level === "HIGH"

            ? "text-red-700"

            : prediction.risk_level === "MEDIUM"

            ? "text-yellow-700"

            : "text-emerald-700"
          }
        `}
      >
        {prediction.disease}
      </h2>

      <p
        className="
          text-xs
          text-gray-500
          mt-2
        "
      >
        {getCountryName(
          prediction.country
        )}
      </p>

    </div>

    {/* RISK BADGE */}

    <div
      className={`
        px-2.5
        py-1
        rounded-full
        text-[10px]
        font-bold
        tracking-wide

        ${
          prediction.risk_level === "HIGH"

          ? "bg-red-100 text-red-700"

          : prediction.risk_level === "MEDIUM"

          ? "bg-yellow-100 text-yellow-700"

          : "bg-emerald-100 text-emerald-700"
        }
      `}
    >
      {prediction.risk_level}
    </div>

  </div>

  {/* SCORE SECTION */}

  <div className="mt-5">

    <div
      className="
        flex
        items-end
        justify-between
      "
    >

      <div>

        <p
          className="
            text-[11px]
            uppercase
            tracking-wide
            text-gray-400
          "
        >
          Combined Score
        </p>

        <h3
          className="
            text-4xl
            font-black
            leading-none
            mt-1
          "
        >
          {prediction.combined_score}
        </h3>

      </div>

      {/* SIGNAL BARS */}

      <div
        className="
          flex
          items-end
          gap-1
          h-10
        "
      >

        <div
          className="
            w-2
            rounded-full
            bg-indigo-400
          "
          style={{
            height: `${
              Math.min(
                prediction.google_score / 50,
                40
              )
            }px`,
          }}
        />

        <div
          className="
            w-2
            rounded-full
            bg-orange-400
          "
          style={{
            height: `${
              Math.min(
                prediction.reddit_score / 10,
                40
              )
            }px`,
          }}
        />

        <div
          className="
            w-2
            rounded-full
            bg-emerald-400
          "
          style={{
            height: `${
              Math.min(
                prediction.who_score,
                40
              )
            }px`,
          }}
        />

      </div>

    </div>

  </div>

  {/* FOOTER */}

  <div
    className="
      mt-4
      pt-3
      border-t
      flex
      justify-between
      items-center
      text-[10px]
      text-gray-400
    "
  >

    <span>
      Geo-aware intelligence
    </span>

    <span>
      Multi-source
    </span>

  </div>

</div>

        ))}

      </div>

    </div>
  )
}
