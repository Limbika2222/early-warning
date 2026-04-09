import { motion } from "framer-motion"

type Props = {
  title: string
  value: string | number
  subtitle?: string
  color?: "blue" | "red" | "green" | "yellow"
  change?: string
}

export default function MetricCard({
  title,
  value,
  subtitle,
  change,
}: Props) {
  const isPositive = change?.startsWith("+")
  const isNegative = change?.startsWith("-")

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`
        bg-white/50
        backdrop-blur-md
        rounded-2xl
        p-6
        border border-white/40
        shadow-md
        transition-all
      `}
    >
      <p className="text-sm text-[#3b6b6f] font-medium tracking-wide">
        {title}
      </p>

      <div className="flex items-center justify-between mt-2">
        <h2 className="text-3xl font-bold text-[#1e3f42]">{value}</h2>

        {change && (
          <span
            className={`
              text-xs px-3 py-1 rounded-full font-medium
              ${
                isPositive
                  ? "bg-[#1f9c94]/15 text-[#1f9c94]"
                  : isNegative
                  ? "bg-red-500/15 text-red-500"
                  : "bg-[#4f8ef7]/15 text-[#4f8ef7]"
              }
            `}
          >
            {change}
          </span>
        )}
      </div>
      {subtitle && (
        <p className="text-xs text-[#3b6b6f] mt-1">{subtitle}</p>
      )}
    </motion.div>
  )
}