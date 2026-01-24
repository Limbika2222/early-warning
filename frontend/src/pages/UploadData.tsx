import { useState } from "react"

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
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!file || !keyword || !country) {
      setStatus("Please select disease, country, and CSV file.")
      return
    }

    setLoading(true)
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
        const errorData: unknown = await res.json()

        if (
          typeof errorData === "object" &&
          errorData !== null &&
          "detail" in errorData
        ) {
          throw new Error(String(errorData.detail))
        }

        throw new Error("Upload failed")
      }

      const data: {
        rows_inserted: number
        date_range: { start: string; end: string }
      } = await res.json()

      setStatus(
        `✅ Uploaded ${data.rows_inserted} rows (${data.date_range.start} → ${data.date_range.end})`
      )
    } catch (err) {
      if (err instanceof Error) {
        setStatus(`❌ ${err.message}`)
      } else {
        setStatus("❌ Upload failed due to an unknown error")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-2">
        Upload Google Trends Data
      </h1>
      <p className="text-gray-600 mb-6">
        Upload <strong>Interest over Time</strong> CSV exported from Google Trends.
      </p>

      <div className="bg-white rounded-lg shadow p-6 space-y-5">
        {/* Disease */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Disease
          </label>
          <select
            value={keyword}
            onChange={e => setKeyword(e.target.value)}
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select disease</option>
            {diseases.map(d => (
              <option key={d.keyword} value={d.keyword}>
                {d.label}
              </option>
            ))}
          </select>
        </div>

        {/* Country */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Country
          </label>
          <select
            value={country}
            onChange={e => setCountry(e.target.value)}
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select country</option>
            {countries.map(c => (
              <option key={c.iso2} value={c.iso2}>
                {c.label}
              </option>
            ))}
          </select>
        </div>

        {/* File */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Google Trends CSV
          </label>
          <input
            type="file"
            accept=".csv"
            onChange={e => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm"
          />
        </div>

        {/* Action */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Uploading…" : "Upload CSV"}
        </button>

        {status && (
          <p className="text-sm mt-2 text-gray-700">{status}</p>
        )}
      </div>
    </div>
  )
}
