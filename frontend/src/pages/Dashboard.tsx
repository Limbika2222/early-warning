import { useState } from "react"
import DiseaseSelector from "../components/dashboard/DiseaseSelector"
import ChartsGrid from "../components/dashboard/ChartsGrid"
import DashboardUploadSelector from "../components/dashboard/DashboardUploadSelector"
import type { UploadHistoryItem } from "../api/trends"

// ---------------------------------
// Helpers
// ---------------------------------
function formatDate(date: Date) {
  return date.toISOString().split("T")[0] // YYYY-MM-DD
}

function getDateRange(days: number) {
  const end = new Date()
  const start = new Date()
  start.setDate(end.getDate() - days)

  return {
    startDate: formatDate(start),
    endDate: formatDate(end),
  }
}

export default function Dashboard() {
  // -------------------------
  // Core state
  // -------------------------
  const [selectedDiseaseId, setSelectedDiseaseId] = useState<number>(1) // Influenza
  const [countryId, setCountryId] = useState<number>(1) // India

  // -------------------------
  // Date range state
  // -------------------------
  const [rangeDays, setRangeDays] = useState<number>(90)

  const { startDate, endDate } = getDateRange(rangeDays)

  // -------------------------
  // MAPPINGS (single source of truth)
  // -------------------------
  const diseaseMap: Record<string, number> = {
    "fever cough": 1,
    malaria: 2,
    cholera: 3,
    zika: 4,
  }

  const countryMap: Record<string, number> = {
    India: 1,
    Malawi: 4,
    Philippines: 5,
  }

  return (
    <div className="space-y-6">
      {/* ---------------------------------
          Upload selector (drives dashboard)
         --------------------------------- */}
      <DashboardUploadSelector
        onSelect={(upload: UploadHistoryItem) => {
          const diseaseId = diseaseMap[upload.keyword]
          const selectedCountryId = countryMap[upload.country]

          if (diseaseId) setSelectedDiseaseId(diseaseId)
          if (selectedCountryId) setCountryId(selectedCountryId)
          // ✅ date range intentionally untouched
        }}
      />

      {/* ---------------------------------
          Controls row
         --------------------------------- */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        {/* Disease cards */}
        <DiseaseSelector
          selectedDiseaseId={selectedDiseaseId}
          onSelect={setSelectedDiseaseId}
        />

        {/* Date range selector */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">Date range:</span>

          <select
            value={rangeDays}
            onChange={e => setRangeDays(Number(e.target.value))}
            className="border rounded px-3 py-2 text-sm"
          >
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
            <option value={180}>Last 6 months</option>
            <option value={365}>Last 12 months</option>
            <option value={365 * 5}>Last 5 years</option>
          </select>
        </div>
      </div>

      {/* ---------------------------------
          Charts
         --------------------------------- */}
      <ChartsGrid
        diseaseId={selectedDiseaseId}
        countryId={countryId}
        startDate={startDate}
        endDate={endDate}
      />
    </div>
  )
}
