import { useState } from "react"
import AppLayout from "../components/layout/AppLayout"
import DiseaseSelector from "../components/dashboard/DiseaseSelector"
import ChartsGrid from "../components/dashboard/ChartsGrid"
import type { Disease } from "../data/mockDashboardData"

export default function Dashboard() {
  const [selectedDisease, setSelectedDisease] =
    useState<Disease>("Influenza")

  return (
    <AppLayout>
      <DiseaseSelector
        selectedDisease={selectedDisease}
        onSelect={setSelectedDisease}
      />
      <ChartsGrid selectedDisease={selectedDisease} />
    </AppLayout>
  )
}
