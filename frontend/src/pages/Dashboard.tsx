import { useState } from "react"
import DiseaseSelector from "../components/dashboard/DiseaseSelector"
import ChartsGrid from "../components/dashboard/ChartsGrid"
import DashboardUploadSelector from "../components/dashboard/DashboardUploadSelector"
import type { UploadHistoryItem } from "../api/trends"

export default function Dashboard() {
  // -------------------------
  // Defaults
  // -------------------------
  const [selectedDiseaseId, setSelectedDiseaseId] = useState<number>(1) // Influenza
  const [countryId, setCountryId] = useState<number>(1) // India

  // -------------------------
  // MAPPINGS (single source of truth)
  // -------------------------
  const diseaseMap: Record<string, number> = {
    "fever cough": 1, // Influenza
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
    <>
      {/* ---------------------------------
          Upload selector (drives dashboard)
         --------------------------------- */}
      <DashboardUploadSelector
        onSelect={(upload: UploadHistoryItem) => {
          const diseaseId = diseaseMap[upload.keyword]
          const selectedCountryId = countryMap[upload.country]

          if (diseaseId) {
            setSelectedDiseaseId(diseaseId)
          }

          if (selectedCountryId) {
            setCountryId(selectedCountryId)
          }
        }}
      />

      {/* ---------------------------------
          Manual disease override
         --------------------------------- */}
      <DiseaseSelector
        selectedDiseaseId={selectedDiseaseId}
        onSelect={setSelectedDiseaseId}
      />

      {/* ---------------------------------
          Charts
         --------------------------------- */}
      <ChartsGrid
        diseaseId={selectedDiseaseId}
        countryId={countryId}
      />
    </>
  )
}
