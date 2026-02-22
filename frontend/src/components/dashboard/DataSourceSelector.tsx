import { motion } from "framer-motion"
import { Activity, Globe, TrendingUp } from "lucide-react"

export type DataSource = "google" | "twitter" | "who"

interface Props {
  value: DataSource
  onChange: (source: DataSource) => void
}

const sources = [
  {
    key: "google" as DataSource,
    label: "Google Trends",
    icon: TrendingUp,
  },
  {
    key: "twitter" as DataSource,
    label: "Twitter",
    icon: Activity,
  },
  {
    key: "who" as DataSource,
    label: "WHO Data",
    icon: Globe,
  },
]

export default function DataSourceSelector({ value, onChange }: Props) {
  return (
    <div className="flex items-center gap-2 bg-white/50 backdrop-blur-md border border-white/40 rounded-xl p-1 shadow-sm w-fit">
      {sources.map((source) => {
        const Icon = source.icon
        const isActive = value === source.key

        return (
          <motion.button
            key={source.key}
            onClick={() => onChange(source.key)}
            whileTap={{ scale: 0.95 }}
            className={`
              relative flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${
                isActive
                  ? "text-white"
                  : "text-[#1e3f42] hover:bg-white/60"
              }
            `}
          >
            {isActive && (
              <motion.div
                layoutId="sourceIndicator"
                className="absolute inset-0 bg-[#1f9c94] rounded-lg -z-10"
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              />
            )}

            <Icon size={16} />
            {source.label}
          </motion.button>
        )
      })}
    </div>
  )
}