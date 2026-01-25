import { useCallback, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { fetchUploadHistory } from "../api/trends"
import type { UploadHistoryItem } from "../api/trends"

type DiseaseOption = {
  label: string
  keyword: string
  diseaseId: number
}

type CountryOption = {
  label: string
  iso2: string
}

const diseases: DiseaseOption[] = [
  { label: "Influenza", keyword: "fever cough", diseaseId: 1 },
  { label: "Malaria", keyword: "malaria", diseaseId: 2 },
  { label: "Cholera", keyword: "cholera", diseaseId: 3 },
  { label: "Zika", keyword: "zika", diseaseId: 4 },
]

const countries: CountryOption[] = [
  { label: "India", iso2: "IN" },
  { label: "Malawi", iso2: "MW" },
  { label: "Philippines", iso2: "PH" },
]

export default function UploadData() {
  const navigate = useNavigate()

  const [keyword, setKeyword] = useState("")
  const [country, setCountry] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  // ---------------------------
  // Upload history table state
  // ---------------------------
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
    } catch {
      setStatus("❌ Failed to fetch upload history")
    } finally {
      setLoadingTable(false)
    }
  }, [])

  useEffect(() => {
    loadUploads()
  }, [loadUploads])

  // ---------------------------
  // Upload handler
  // ---------------------------
  const handleSubmit = async () => {
    if (!file || !keyword || !country) {
      setStatus("Please select disease, country, and CSV file.")
      return
    }

    setUploading(true)
    setStatus(null)

    try {
      const formData = new FormData()
      formData.append("file", file)
      formData.append("disease_keyword", keyword)
      formData.append("country_iso2", country)

      const res = await fetch("/api/trends/upload-csv", {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        const errorData = (await res.json()) as { detail?: string }
        throw new Error(errorData.detail ?? "Upload failed")
      }

      const data = (await res.json()) as {
        rows_inserted: number
        date_range: { start: string; end: string }
      }

      setStatus(
        `✅ Uploaded ${data.rows_inserted} rows (${data.date_range.start} → ${data.date_range.end})`
      )

      await loadUploads()
    } catch (err) {
      setStatus(err instanceof Error ? `❌ ${err.message}` : "❌ Upload failed")
    } finally {
      setUploading(false)
    }
  }

  // ---------------------------
  // Helper: keyword → diseaseId
  // ---------------------------
  const getDiseaseIdFromKeyword = (kw: string) =>
    diseases.find(d => d.keyword === kw)?.diseaseId

  return (
    <div className="max-w-5xl mx-auto p-8 space-y-12">
      {/* Upload Form */}
      <div>
        <h1 className="text-2xl font-semibold mb-6">
          Upload Google Trends Data
        </h1>

        <div className="bg-white p-6 rounded shadow space-y-5">
          <select
            className="w-full border rounded px-3 py-2"
            value={keyword}
            onChange={e => setKeyword(e.target.value)}
          >
            <option value="">Select disease</option>
            {diseases.map(d => (
              <option key={d.keyword} value={d.keyword}>
                {d.label}
              </option>
            ))}
          </select>

          <select
            className="w-full border rounded px-3 py-2"
            value={country}
            onChange={e => setCountry(e.target.value)}
          >
            <option value="">Select country</option>
            {countries.map(c => (
              <option key={c.iso2} value={c.iso2}>
                {c.label}
              </option>
            ))}
          </select>

          <input
            type="file"
            accept=".csv"
            onChange={e => setFile(e.target.files?.[0] ?? null)}
          />

          <button
            onClick={handleSubmit}
            disabled={uploading}
            className="bg-blue-600 text-white px-6 py-2 rounded"
          >
            {uploading ? "Uploading…" : "Upload CSV"}
          </button>

          {status && <p className="text-sm">{status}</p>}
        </div>
      </div>

      {/* Upload History Table */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Upload History (click row to open dashboard)
        </h2>

        {loadingTable ? (
          <p>Loading uploads…</p>
        ) : (
          <table className="w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 border">Keyword</th>
                <th className="p-2 border">Country</th>
                <th className="p-2 border">Rows</th>
                <th className="p-2 border">Uploaded at</th>
              </tr>
            </thead>
            <tbody>
              {uploads.map(u => {
                const diseaseId = getDiseaseIdFromKeyword(u.keyword)

                return (
                  <tr
                    key={u.id}
                    className="cursor-pointer hover:bg-blue-50"
                    onClick={() => {
                      if (diseaseId) {
                        navigate(`/dashboard?diseaseId=${diseaseId}`)
                      }
                    }}
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
                )
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
