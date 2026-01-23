interface Props {
  label: string
  active: boolean
  onClick: () => void
}

export default function DiseaseCard({ label, active, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      className={`p-5 rounded-xl border cursor-pointer transition-all
        ${active
          ? "bg-blue-600 text-white shadow-lg"
          : "bg-white hover:shadow-md"}`}
    >
      <div className="text-sm opacity-80 mb-2">Disease</div>
      <div className="text-lg font-semibold">{label}</div>
    </div>
  )
}
