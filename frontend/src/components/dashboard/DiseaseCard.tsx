import { motion } from "framer-motion"
import type { ReactNode } from "react"

interface Props {
  label: string
  description?: string
  icon?: ReactNode
  active: boolean
  onClick: () => void
}

export default function DiseaseCard({
  label,
  description,
  icon,
  active,
  onClick,
}: Props) {
  return (
    <motion.button
      type="button"
      onClick={onClick}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      className={`
        relative w-full text-left p-6 rounded-2xl
        transition-all duration-300
        backdrop-blur-md
        border
        ${
          active
            ? "bg-white/70 border-[#1f9c94] shadow-md"
            : "bg-white/40 border-white/40 hover:bg-white/60"
        }
      `}
    >
      {/* Active glow */}
      {active && (
        <motion.div
          layoutId="activeDiseaseGlow"
          className="absolute inset-0 rounded-2xl bg-gradient-to-br from-[#1f9c94]/10 to-[#4f8ef7]/10 pointer-events-none"
        />
      )}

      <div className="relative z-10 space-y-3">
        {/* Header */}
        <div className="flex items-center gap-3">
          {icon && (
            <div className="text-[#1f9c94] text-xl">
              {icon}
            </div>
          )}
          <h3 className="text-lg font-semibold text-[#1e3f42]">
            {label}
          </h3>
        </div>

        {/* Description */}
        {description && (
          <p className="text-sm text-[#3b6b6f] leading-relaxed">
            {description}
          </p>
        )}

        {/* Status */}
        <div className="text-xs mt-2">
          {active ? (
            <span className="text-[#1f9c94] font-medium">
              Monitoring Active
            </span>
          ) : (
            <span className="text-[#5a7c7f]">
              Click to monitor
            </span>
          )}
        </div>
      </div>
    </motion.button>
  )
}
