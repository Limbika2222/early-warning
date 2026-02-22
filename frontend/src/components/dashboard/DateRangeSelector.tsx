import { motion } from "framer-motion"

interface Props {
  startDate: string | null
  endDate: string | null
  onChange: (range: {
    startDate: string | null
    endDate: string | null
  }) => void
}

export default function DateRangeSelector({
  startDate,
  endDate,
  onChange,
}: Props) {
  const today = new Date().toISOString().split("T")[0]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="
        flex items-center gap-3
        bg-white/60
        backdrop-blur-md
        border border-white/40
        rounded-xl
        px-3 py-2
        shadow-sm
      "
    >
      {/* Start */}
      <input
        type="date"
        max={today}
        value={startDate ?? ""}
        onChange={(e) =>
          onChange({
            startDate: e.target.value || null,
            endDate,
          })
        }
        className="
          bg-white/80
          border border-white/50
          rounded-md
          px-2 py-1
          text-sm
          text-[#1e3f42]
          focus:outline-none
          focus:ring-2
          focus:ring-[#1f9c94]
          transition
        "
      />

      <span className="text-[#3b6b6f] text-sm">–</span>

      {/* End */}
      <input
        type="date"
        max={today}
        value={endDate ?? ""}
        onChange={(e) =>
          onChange({
            startDate,
            endDate: e.target.value || null,
          })
        }
        className="
          bg-white/80
          border border-white/50
          rounded-md
          px-2 py-1
          text-sm
          text-[#1e3f42]
          focus:outline-none
          focus:ring-2
          focus:ring-[#1f9c94]
          transition
        "
      />

      {(startDate || endDate) && (
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() =>
            onChange({
              startDate: null,
              endDate: null,
            })
          }
          className="
            text-xs
            text-[#1f9c94]
            font-medium
            ml-2
            hover:underline
          "
        >
          Clear
        </motion.button>
      )}
    </motion.div>
  )
}