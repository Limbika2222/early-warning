import { useState } from "react"

type DiseaseOption = {
  id: number
  name: string
}

type CountryOption = {
  id: number
  name: string
}

const diseases: DiseaseOption[] = [
  { id: 1, name: "Influenza" },
  { id: 2, name: "Malaria" },
  { id: 3, name: "Cholera" },
  { id: 4, name: "Zika" },
]

const countries: CountryOption[] = [
  { id: 1, name: "India" },
  { id: 2, name: "Malawi" },
  { id: 3, name: "Philippines" },
]

export default function UploadData() {
  const [diseaseId, setDiseaseId] = useState<number | "">("")
  const [countryId, setCountryId] = useState<number | "">("")
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!file || !diseaseId || !countryId) {
      setStatus("Please select disease, country, and CSV file.")
      return
    }

    setLoading(true)
    setStatus(null)

    try {
      // Backend upload will be connected next
      console.log("Uploading:", {
        diseaseId,
        countryId,
        file,
      })

      await new Promise(resolve => setTimeout(resolve, 1000)) // mock delay

      setStatus("✅ CSV uploaded successfully")
    } catch {
      setStatus("❌ Upload failed")
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
        Upload Google Trends <strong>Interest over Time</strong> CSV files for analysis.
      </p>

      <div className="bg-white rounded-lg shadow p-6 space-y-5">
        {/* Disease */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Disease
          </label>
          <select
            value={diseaseId}
            onChange={e => setDiseaseId(Number(e.target.value))}
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select disease</option>
            {diseases.map(d => (
              <option key={d.id} value={d.id}>
                {d.name}
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
            value={countryId}
            onChange={e => setCountryId(Number(e.target.value))}
            className="w-full border rounded px-3 py-2"
          >
            <option value="">Select country</option>
            {countries.map(c => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        {/* File */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Google Trends CSV file
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
