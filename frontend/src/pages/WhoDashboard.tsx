import { useEffect, useState } from "react"
import { formatDistanceToNow } from "date-fns"
import axios from "axios"

import {
  fetchOutbreakHistory,
  fetchDiseaseSummary,
  fetchCountrySummary,
} from "../api/who"

import type {
  WhoReport,
  DiseaseSummary,
  CountrySummary,
} from "../api/who"

import OutbreakMap from "../components/who/OutbreakMap"

const RAW_BASE = import.meta.env.VITE_API_BASE

if (!RAW_BASE) {
  throw new Error(
    "VITE_API_BASE missing"
  )
}

const CLEAN_BASE = RAW_BASE.endsWith("/")
  ? RAW_BASE.slice(0, -1)
  : RAW_BASE

const API_BASE = `${CLEAN_BASE}`

// =====================================================
// SEVERITY COLORS
// =====================================================

function getSeverityClasses(
  severity: string
) {

  switch (severity) {

    case "CRITICAL":

      return `
        bg-red-100
        text-red-700
        border border-red-200
      `

    case "HIGH":

      return `
        bg-orange-100
        text-orange-700
        border border-orange-200
      `

    case "MEDIUM":

      return `
        bg-yellow-100
        text-yellow-700
        border border-yellow-200
      `

    default:

      return `
        bg-blue-100
        text-blue-700
        border border-blue-200
      `
  }
}

function formatRelativeTime(
  dateString?: string
) {

  if (!dateString) {

    return "Unknown time"
  }

  try {

    const parsedDate = new Date(
      dateString
    )

    return formatDistanceToNow(
      parsedDate,
      {
        addSuffix: true,
      }
    )

  } catch {

    return "Unknown time"
  }
}

export default function WhoDashboard() {

  const [reports, setReports] = useState<WhoReport[]>([])

  const [diseases, setDiseases] = useState<DiseaseSummary[]>([])

  const [countries, setCountries] = useState<CountrySummary[]>([])

  const [
    countryDiseases,
    setCountryDiseases,
  ] = useState<
    Record<string, string[]>
  >({})

  const [loading, setLoading] = useState(true)

  // =====================================================
  // LOAD DATA
  // =====================================================

  async function loadDashboard() {
    try {
      setLoading(true)
      const [
        history,
        diseaseSummary,
        countrySummary,
      ] = await Promise.all([
        fetchOutbreakHistory(),
        fetchDiseaseSummary(),
        fetchCountrySummary(),
      ])

      const reportsData = history.reports;
      const diseaseMap: Record<
        string,
        Set<string>
      > = {}

      reportsData.forEach((report) => {
        const iso2 =
          report.country.iso2
        if (!iso2) return
        if (!diseaseMap[iso2]) {
          diseaseMap[iso2] =
            new Set()
        }
        diseaseMap[iso2].add(
          report.disease
        )
      })

      const finalMap: Record<
        string,
        string[]
      > = {}

      Object.entries(diseaseMap).forEach(
        ([iso2, diseases]) => {
          finalMap[iso2] =
            Array.from(diseases)
        }
      )

      setCountryDiseases(finalMap)
      setReports(history.reports)
      setDiseases(diseaseSummary.diseases)
      setCountries(countrySummary.countries)
    } catch (err) {
      console.error(
        "WHO dashboard error:",
        err
      )
    } finally {
      setLoading(false)
    }
  }


  useEffect(() => {
    loadDashboard()
  }, [])

  const refreshWHOData = async () => {
    try {
      setLoading(true)
      await axios.post(
        `${API_BASE}/api/who/refresh`
      )
      await loadDashboard()
    } catch (error) {
      console.error(
        "WHO refresh failed",
        error
      )
    } finally {
      setLoading(false)
    }
  }

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return (
      <div className="p-6 text-gray-500">
        Loading WHO intelligence...
      </div>
    )
  }

  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="p-6 space-y-6 bg-[#f7faf9] min-h-screen">

      {/* HEADER */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-[#1e3f42]">
            WHO / Official Outbreak Intelligence
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Persistent outbreak intelligence powered by GDELT
          </p>
        </div>
        <button
          onClick={refreshWHOData}
          className="
            px-4 py-2
            bg-emerald-600
            hover:bg-emerald-700
            text-white
            rounded-xl
            text-sm
            font-medium
            transition
          "
        >
          Refresh WHO Data
        </button>
      </div>


      {/* SUMMARY CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

        <div
          className="
            bg-white rounded-2xl
            shadow-sm p-5 border
          "
        >

          <p className="text-sm text-gray-500">
            Total Outbreak Reports
          </p>

          <h2 className="text-4xl font-bold mt-3 text-[#1e3f42]">
            {reports.length}
          </h2>

        </div>

        <div
          className="
            bg-white rounded-2xl
            shadow-sm p-5 border
          "
        >

          <p className="text-sm text-gray-500">
            Diseases Detected
          </p>

          <h2 className="text-4xl font-bold mt-3 text-[#1e3f42]">
            {diseases.length}
          </h2>

        </div>

        <div
          className="
            bg-white rounded-2xl
            shadow-sm p-5 border
          "
        >

          <p className="text-sm text-gray-500">
            Countries Affected
          </p>

          <h2 className="text-4xl font-bold mt-3 text-[#1e3f42]">
            {countries.length}
          </h2>

        </div>

      </div>

      <OutbreakMap
        countries={countries}
        diseaseMap={countryDiseases}
      />

      {/* DISEASE SUMMARY */}
      <div
        className="
          bg-white rounded-2xl
          shadow-sm p-5 border
        "
      >

        <div className="flex items-center justify-between mb-5">

          <h2 className="text-xl font-semibold text-[#1e3f42]">
            Disease Rankings
          </h2>

          <span className="text-xs text-gray-400">
            Official outbreak intelligence
          </span>

        </div>

        <div className="space-y-3">

          {diseases.map((disease) => (

            <div
              key={disease.disease}
              className="
                flex justify-between items-center
                border rounded-xl px-4 py-3
                hover:bg-gray-50 transition
              "
            >

              <span className="font-medium">
                {disease.disease}
              </span>

              <span
                className="
                  text-sm font-semibold
                  bg-[#1f9c94]/10
                  text-[#1f9c94]
                  px-3 py-1 rounded-full
                "
              >
                {disease.count}
              </span>

            </div>

          ))}

        </div>

      </div>

      {/* COUNTRY SUMMARY */}
      <div
        className="
          bg-white rounded-2xl
          shadow-sm p-5 border
        "
      >

        <div className="flex items-center justify-between mb-5">

          <h2 className="text-xl font-semibold text-[#1e3f42]">
            Country Outbreak Summary
          </h2>

          <span className="text-xs text-gray-400">
            Geo-aware outbreak aggregation
          </span>

        </div>

        <div className="space-y-3">

          {countries.map((country) => (

            <div
              key={country.country_iso2}
              className="
                flex justify-between items-center
                border rounded-xl px-4 py-3
                hover:bg-gray-50 transition
              "
            >

              <div className="flex items-center gap-3">

                <span className="font-medium">
                  {country.country_name || "Unknown"}
                </span>

                <span
                  className="
                    text-xs bg-gray-100
                    text-gray-500
                    px-2 py-1 rounded-full
                  "
                >
                  {country.country_iso2}
                </span>

              </div>

              <span
                className="
                  text-sm font-semibold
                  bg-[#1f9c94]/10
                  text-[#1f9c94]
                  px-3 py-1 rounded-full
                "
              >
                {country.outbreak_count}
              </span>

            </div>

          ))}

        </div>

      </div>

      {/* OUTBREAK FEED */}
      <div
        className="
          bg-white rounded-2xl
          shadow-sm p-5 border
        "
      >

        <div className="flex items-center justify-between mb-5">

          <h2 className="text-xl font-semibold text-[#1e3f42]">
            Historical Outbreak Feed
          </h2>

          <span className="text-xs text-gray-400">
            Live epidemiological intelligence
          </span>

        </div>

        <div className="space-y-4">

          {reports.map((report) => (

            <div
              key={report.url}
              className="
                border rounded-2xl p-5
                hover:shadow-md
                hover:border-[#1f9c94]/20
                transition-all duration-300
                bg-white
              "
            >

              <div className="flex justify-between gap-4">

                <div className="flex-1">

                  <div className="flex items-start gap-3 flex-wrap">

                    <h3
                      className="
                        font-semibold
                        text-[#1e3f42]
                        text-lg
                      "
                    >
                      {report.title}
                    </h3>

                    <span
                      className={`
                        px-3 py-1 rounded-full
                        text-[11px]
                        font-bold
                        ${getSeverityClasses(
                          report.severity
                        )}
                      `}
                    >
                      {report.severity}
                    </span>

                  </div>

                  <div
                    className="
                      flex gap-3 mt-4
                      text-sm text-gray-500
                      flex-wrap
                    "
                  >

                    <span
                      className="
                        bg-gray-100
                        px-3 py-1 rounded-full
                      "
                    >
                      Disease: {report.disease}
                    </span>

                    <span
                      className="
                        bg-gray-100
                        px-3 py-1 rounded-full
                      "
                    >
                      Country:
                      {" "}
                      {report.country.name || "Unknown"}
                    </span>

                    <span
                      className="
                        bg-gray-100
                        px-3 py-1 rounded-full
                      "
                    >
                      Source:
                      {" "}
                      {report.source}
                    </span>

                    <span
                      className="
                        bg-[#1f9c94]/10
                        text-[#1f9c94]
                        px-3 py-1 rounded-full
                        font-medium
                      "
                    >
                      {formatRelativeTime(
                        report.ingested_at
                      )}
                    </span>

                  </div>

                </div>

                <a
                  href={report.url}
                  target="_blank"
                  rel="noreferrer"
                  className="
                    h-fit
                    text-[#1f9c94]
                    text-sm
                    font-semibold
                    hover:underline
                  "
                >
                  Open
                </a>

              </div>

            </div>

          ))}

        </div>

      </div>

    </div>
  )
}
