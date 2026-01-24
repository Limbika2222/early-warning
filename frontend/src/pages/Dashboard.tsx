import { useState } from "react"
import AppLayout from "../components/layout/AppLayout"
import DiseaseSelector from "../components/dashboard/DiseaseSelector"
import ChartsGrid from "../components/dashboard/ChartsGrid"

export default function Dashboard() {
  // Default = Influenza
  const [selectedDiseaseId, setSelectedDiseaseId] = useState<number>(1)

  // India for now
  const countryId = 1

  return (
    <AppLayout>
      <DiseaseSelector
        selectedDiseaseId={selectedDiseaseId}
        onSelect={setSelectedDiseaseId}
      />

      <ChartsGrid
        keywordId={selectedDiseaseId}
        countryId={countryId}
      />
    </AppLayout>
  )
}
