import { useEffect, useState } from "react"
import { fetchUploadHistory } from "../../api/trends"
import type { UploadHistoryItem } from "../../api/trends"

interface Props {
  onSelect: (upload: UploadHistoryItem) => void
}

export default function DashboardUploadSelector({ onSelect }: Props) {
  const [uploads, setUploads] = useState<UploadHistoryItem[]>([])
  const [selectedId, setSelectedId] = useState<number | "">("")

  useEffect(() => {
    fetchUploadHistory().then(setUploads)
  }, [])

  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        View uploaded dataset
      </label>

      <select
        className="w-full border rounded px-3 py-2"
        value={selectedId}
        onChange={e => {
          const id = Number(e.target.value)
          setSelectedId(id)
          const upload = uploads.find(u => u.id === id)
          if (upload) onSelect(upload)
        }}
      >
        <option value="">Select dataset</option>

        {uploads.map(u => (
          <option key={u.id} value={u.id}>
            {u.keyword} – {u.country} –{" "}
            {new Date(u.uploaded_at).toLocaleDateString()}
          </option>
        ))}
      </select>
    </div>
  )
}
