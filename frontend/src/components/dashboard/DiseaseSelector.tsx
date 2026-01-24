import DiseaseCard from "./DiseaseCard"

export type Disease = {
  id: number
  label: string
}

interface Props {
  selectedDiseaseId: number
  onSelect: (id: number) => void
}

const diseases: Disease[] = [
  { id: 1, label: "Influenza" },
  { id: 20, label: "Malaria" },   // IMPORTANT: matches DB
  { id: 30, label: "Cholera" },
  { id: 42, label: "Zika" },
]

export default function DiseaseSelector({
  selectedDiseaseId,
  onSelect,
}: Props) {
  return (
    <div className="grid grid-cols-4 gap-6 mb-8">
      {diseases.map(d => (
        <DiseaseCard
          key={d.id}
          label={d.label}
          active={d.id === selectedDiseaseId}
          onClick={() => onSelect(d.id)}
        />
      ))}
    </div>
  )
}
