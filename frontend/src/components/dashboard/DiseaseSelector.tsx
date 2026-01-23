import DiseaseCard from "./DiseaseCard"
import type { Disease } from "../../data/mockDashboardData"

interface Props {
  selectedDisease: Disease
  onSelect: (disease: Disease) => void
}

const diseases: Disease[] = [
  "Influenza",
  "Malaria",
  "Cholera",
  "Zika",
]

export default function DiseaseSelector({
  selectedDisease,
  onSelect,
}: Props) {
  return (
    <div className="grid grid-cols-4 gap-6 mb-8">
      {diseases.map(d => (
        <DiseaseCard
          key={d}
          label={d}
          active={d === selectedDisease}
          onClick={() => onSelect(d)}
        />
      ))}
    </div>
  )
}
