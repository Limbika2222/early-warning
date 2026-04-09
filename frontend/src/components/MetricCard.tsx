type CardColor = "blue" | "red" | "green" | "yellow"

interface Props {
  title: string
  value: string | number
  subtitle?: string
  color?: CardColor
}

const colorStyles: Record<CardColor, string> = {
  blue: "bg-blue-500/10 text-blue-500 border-blue-500/20",
  red: "bg-red-500/10 text-red-500 border-red-500/20",
  green: "bg-green-500/10 text-green-500 border-green-500/20",
  yellow: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
}

export default function MetricCard({
  title,
  value,
  subtitle,
  color = "blue",
}: Props) {
  return (
    <div className={`rounded-2xl border p-6 shadow-sm ${colorStyles[color]}`}>
      <div className="flex flex-col">
        <span className="text-sm opacity-70">{title}</span>
        <span className="text-3xl font-bold mt-2">{value}</span>
        {subtitle && (
          <span className="text-xs opacity-60 mt-1">{subtitle}</span>
        )}
      </div>
    </div>
  )
}