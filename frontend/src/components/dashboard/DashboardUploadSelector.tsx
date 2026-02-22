import { useEffect, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Database, ChevronDown } from "lucide-react"

import { fetchUploadHistory } from "../../api/trends"
import type { UploadHistoryItem } from "../../api/trends"

interface Props {
  onSelect: (upload: UploadHistoryItem) => void
}

export default function DashboardUploadSelector({ onSelect }: Props) {
  const [uploads, setUploads] = useState<UploadHistoryItem[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [isOpen, setIsOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUploadHistory()
      .then(setUploads)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-4">
      {/* Header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="
          w-full
          flex items-center justify-between
          text-[#1e3f42]
          font-semibold
        "
      >
        <div className="flex items-center gap-2">
          <Database size={18} />
          <span>Uploaded Datasets</span>
        </div>

        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown size={18} />
        </motion.div>
      </button>

      {/* Collapsible Content */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            {loading ? (
              <div className="text-sm text-[#3b6b6f] py-4">
                Loading datasets...
              </div>
            ) : uploads.length === 0 ? (
              <div className="text-sm text-[#3b6b6f] py-4">
                No uploaded datasets found
              </div>
            ) : (
              <div className="max-h-56 overflow-y-auto space-y-2 pr-1 mt-3">
                {uploads.map((upload) => {
                  const isActive = selectedId === upload.id

                  return (
                    <motion.div
                      key={upload.id}
                      whileHover={{ y: -2 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => {
                        setSelectedId(upload.id)
                        onSelect(upload)
                      }}
                      className={`
                        cursor-pointer
                        p-4
                        rounded-xl
                        border
                        backdrop-blur-md
                        transition-all
                        ${
                          isActive
                            ? "bg-[#1f9c94]/15 border-[#1f9c94]/40"
                            : "bg-white/40 border-white/40 hover:bg-white/60"
                        }
                      `}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="text-sm font-medium text-[#1e3f42]">
                            {upload.keyword}
                          </p>
                          <p className="text-xs text-[#3b6b6f] mt-1">
                            {upload.country}
                          </p>
                        </div>

                        <div className="text-xs text-[#3b6b6f]">
                          {new Date(upload.uploaded_at).toLocaleDateString()}
                        </div>
                      </div>
                    </motion.div>
                  )
                })}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}