import type { ReactNode } from "react"
import { motion } from "framer-motion"

interface Props {
  title: string
  children: ReactNode
}

export default function ChartCard({ title, children }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="
        bg-white/50
        backdrop-blur-md
        rounded-2xl
        p-6
        border border-white/40
        shadow-md
        transition-all
      "
    >
      <h3 className="text-sm font-semibold text-[#1e3f42] mb-4 tracking-wide">
        {title}
      </h3>

      {children}
    </motion.div>
  )
}
