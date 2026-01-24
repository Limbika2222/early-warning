import { useCallback, useEffect, useState } from "react"
import { fetchUploadedDatasets } from "../api/trends"
import type { UploadedDataset } from "../api/trends"

type DiseaseOption = {
  label: string
  keyword: string
}

type CountryOption = {
  label: string
  iso2: string
}

const diseases: DiseaseOption[] = [
  { label: "Influenza", keyword: "fever cough" },
  { label: "Malaria", keyword: "malaria" },
  { label: "Cholera", keyword: "cholera" },
  { label: "Zika", keyword: "zika" },
]

const countries: CountryOption[] = [
  { label: "India", iso2: "IN" },
  { label: "Malawi", iso2: "MW" },
  { label: "Philippines", iso2: "PH" },
]

export default function UploadData() {
  const [keyword, setKeyword] = useState("")
  const [country, setCountry] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  // ---------------------------
  // Dataset table state
  // ---------------------------
  const [datasets, setDatasets] = useState<UploadedDataset[]>([])
  const [search, setSearch] = useState("")
  const [sortBy, setSortBy] =
    useState<"upload_date" | "keyword" | "country">("upload_date")
  const [order, setOrder] = useState<"asc" | "desc">("desc")
  const [loadingTable, setLoadingTable] = useState(false)

  // ---------------------------
  // Load datasets (memoized)
  // ---------------------------
  const loadDatasets = useCallback(async () => {
    setLoadingTable(true)
    try {
      const data = await fetchUploadedDatasets({
        search,
        sort_by: sortBy,
        order,
      })
      setDatasets(data)
    } finally {
      setLoadingTable(false)
    }
  }, [search, sortBy, order])

  useEffect(() => {
    loadDatasets()
  }, [loadDatasets])

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

      await loadDatasets()
    } catch (err) {
      setStatus(err instanceof Error ? `❌ ${err.message}` : "❌ Upload failed")
    } finally {
      setUploading(false)
    }
  }

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

      {/* Dataset Table */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Uploaded Datasets
        </h2>

        <div className="flex gap-4 mb-4">
          <input
            className="border px-3 py-2 rounded"
            placeholder="Search keyword"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />

          <select
            className="border px-3 py-2 rounded"
            value={sortBy}
            onChange={e => setSortBy(e.target.value as typeof sortBy)}
          >
            <option value="upload_date">Upload date</option>
            <option value="keyword">Keyword</option>
            <option value="country">Country</option>
          </select>

          <button
            className="border px-3 py-2 rounded"
            onClick={() => setOrder(o => (o === "asc" ? "desc" : "asc"))}
          >
            {order}
          </button>
        </div>

        {loadingTable ? (
          <p>Loading datasets…</p>
        ) : (
          <table className="w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 border">Keyword</th>
                <th className="p-2 border">Country</th>
                <th className="p-2 border">Date range</th>
                <th className="p-2 border">Rows</th>
                <th className="p-2 border">Uploaded</th>
              </tr>
            </thead>
            <tbody>
              {datasets.map((d, i) => (
                <tr key={i}>
                  <td className="p-2 border">{d.keyword}</td>
                  <td className="p-2 border">{d.country}</td>
                  <td className="p-2 border">
                    {d.start_date} → {d.end_date}
                  </td>
                  <td className="p-2 border text-center">{d.row_count}</td>
                  <td className="p-2 border">
                    {new Date(d.upload_date).toLocaleString()}
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
