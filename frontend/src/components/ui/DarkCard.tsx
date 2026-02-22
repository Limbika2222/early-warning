import { motion } from "framer-motion"
import type { ReactNode } from "react"

type Props = {
  children: ReactNode
  className?: string
}

export default function DarkCard({ children, className = "" }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={`bg-[#1e1f2f] rounded-2xl shadow-xl p-6 ${className}`}
    >
      {children}
    </motion.div>
  )
}
