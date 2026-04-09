import { useCallback, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { fetchUploadHistory } from "../api/trends"
import { runAnalysis } from "../api/signal"
import type { UploadHistoryItem } from "../api/trends"

const API_BASE = import.meta.env.VITE_API_BASE

type CountryOption = {
  label: string
  id: number
}

const countries: CountryOption[] = [
  { label: "India", id: 1 },
  { label: "Malawi", id: 2 },
  { label: "Philippines", id: 3 },
]

export default function UploadData() {
  const navigate = useNavigate()

  const [countryId, setCountryId] = useState<number | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  const [uploads, setUploads] = useState<UploadHistoryItem[]>([])
  const [loadingTable, setLoadingTable] = useState(false)

  // ---------------------------
  // Load upload history
  // ---------------------------
  const loadUploads = useCallback(async () => {
    setLoadingTable(true)
    try {
      const data = await fetchUploadHistory()
      setUploads(data)
    } catch (err) {
      console.error("Upload history error:", err)
      setStatus("❌ Failed to fetch upload history")
    } finally {
      setLoadingTable(false)
    }
  }, [])

  useEffect(() => {
    loadUploads()
  }, [loadUploads])

  // ---------------------------
  // Submit handler (FIXED)
  // ---------------------------
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault() // 🔥 VERY IMPORTANT

    if (!file || !countryId) {
      setStatus("❌ Please select a country and CSV file.")
      return
    }

    console.log("Uploading file:", file)
    console.log("Country ID:", countryId)

    setUploading(true)
    setStatus(null)

    try {
      const formData = new FormData()
      formData.append("file", file)
      formData.append("country_id", String(countryId))

      const response = await fetch(`${API_BASE}/api/trends/upload-csv`, {
        method: "POST",
        body: formData,
      })

      console.log("Response status:", response.status)

      if (!response.ok) {
        const text = await response.text()
        console.error("Upload failed:", text)
        throw new Error(text || "Upload failed")
      }

      const data = await response.json()
      console.log("Upload success:", data)

      // 🔥 run backend analysis
      await runAnalysis()

      setStatus(
        `✅ Uploaded ${data.rows_processed} rows (${data.keywords_processed} keywords)`
      )

      // reset
      setFile(null)
      setCountryId(null)

      await loadUploads()

      // 🔥 force dashboard refresh
      navigate(`/dashboard?refresh=${Date.now()}`)

    } catch (err) {
      console.error("Upload error:", err)
      setStatus(
        err instanceof Error ? `❌ ${err.message}` : "❌ Upload failed"
      )
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-8 space-y-12">

      {/* ---------------- Upload Form ---------------- */}
      <form onSubmit={handleSubmit}>
        <h1 className="text-2xl font-semibold mb-6">
          Upload Google Trends Data
        </h1>

        <div className="bg-white p-6 rounded shadow space-y-5">

          {/* COUNTRY */}
          <select
            id="country"
            name="country"
            className="w-full border rounded px-3 py-2"
            value={countryId ?? ""}
            onChange={(e) => setCountryId(Number(e.target.value))}
          >
            <option value="">Select country</option>
            {countries.map((c) => (
              <option key={c.id} value={c.id}>
                {c.label}
              </option>
            ))}
          </select>

          {/* FILE INPUT */}
          <input
            id="file"
            name="file"
            type="file"
            accept=".csv"
            className="w-full"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />

          {/* BUTTON */}
          <button
            type="submit"
            disabled={uploading}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-60"
          >
            {uploading ? "Uploading…" : "Upload & Analyze"}
          </button>

          {/* STATUS */}
          {status && <p className="text-sm">{status}</p>}
        </div>
      </form>

      {/* ---------------- Upload History ---------------- */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Upload History
        </h2>

        {loadingTable ? (
          <p>Loading uploads…</p>
        ) : uploads.length === 0 ? (
          <p className="text-gray-500">No uploads yet.</p>
        ) : (
          <table className="w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 border">Keyword</th>
                <th className="p-2 border">Country</th>
                <th className="p-2 border">Rows</th>
                <th className="p-2 border">Uploaded</th>
              </tr>
            </thead>
            <tbody>
              {uploads.map((u) => (
                <tr
                  key={u.id}
                  className="cursor-pointer hover:bg-indigo-50"
                  onClick={() =>
                    navigate(`/dashboard?refresh=${Date.now()}`)
                  }
                >
                  <td className="p-2 border">{u.keyword}</td>
                  <td className="p-2 border">{u.country}</td>
                  <td className="p-2 border text-center">
                    {u.rows_inserted}
                  </td>
                  <td className="p-2 border">
                    {new Date(u.uploaded_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}