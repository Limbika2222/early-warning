import DiseaseCard from "./DiseaseCard"

export type Disease = {
  id: number
  label: string
}

interface Props {
  selectedDiseaseId: number
  onSelect: (id: number) => void
}

/**
 * IMPORTANT:
 * These IDs MUST match the `diseases.id` values in the database
 *
 * 1 → Influenza
 * 2 → Malaria
 * 3 → Cholera
 * 4 → Zika
 */
const diseases: Disease[] = [
  { id: 1, label: "Influenza" },
  { id: 2, label: "Malaria" },
  { id: 3, label: "Cholera" },
  { id: 4, label: "Zika" },
]

export default function DiseaseSelector({
  selectedDiseaseId,
  onSelect,
}: Props) {
  return (
    <div className="grid grid-cols-4 gap-6 mb-8">
      {diseases.map(disease => (
        <DiseaseCard
          key={disease.id}
          label={disease.label}
          active={disease.id === selectedDiseaseId}
          onClick={() => onSelect(disease.id)}
        />
      ))}
    </div>
  )
}
