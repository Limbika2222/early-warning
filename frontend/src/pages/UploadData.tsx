"use client"

import { useCallback, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

import {
  fetchCountries,
  fetchUploadHistory,
  type UploadHistoryItem,
  type Country,
} from "../api/trends"

import { runAnalysis } from "../api/signal"

const API_BASE = import.meta.env.VITE_API_BASE

export default function UploadData() {
  const navigate = useNavigate()

  // =====================================================
  // State
  // =====================================================

  const [countries, setCountries] = useState<
    Country[]
  >([])

  const [countryId, setCountryId] =
    useState<number | null>(null)

  const [file, setFile] = useState<File | null>(
    null
  )

  const [status, setStatus] = useState<
    string | null
  >(null)

  const [uploading, setUploading] =
    useState(false)

  const [uploads, setUploads] = useState<
    UploadHistoryItem[]
  >([])

  const [loadingTable, setLoadingTable] =
    useState(false)

  const [loadingCountries, setLoadingCountries] =
    useState(false)

  // =====================================================
  // Load countries
  // =====================================================

  const loadCountries = useCallback(async () => {
    setLoadingCountries(true)

    try {
      const data = await fetchCountries()

      console.log("🌍 Countries:", data)

      setCountries(data || [])

    } catch (err) {
      console.error("❌ Countries error:", err)

      setStatus("❌ Failed to load countries")

    } finally {
      setLoadingCountries(false)
    }
  }, [])

  // =====================================================
  // Load uploads
  // =====================================================

  const loadUploads = useCallback(async () => {
    setLoadingTable(true)

    try {
      const data = await fetchUploadHistory()

      console.log("🔥 Uploads:", data)

      setUploads(data || [])

    } catch (err) {
      console.error(
        "❌ Upload history error:",
        err
      )

      setUploads([])

      setStatus(
        "❌ Failed to fetch upload history"
      )

    } finally {
      setLoadingTable(false)
    }
  }, [])

  // =====================================================
  // Initial load
  // =====================================================

  useEffect(() => {
    loadCountries()
    loadUploads()
  }, [loadCountries, loadUploads])

  // =====================================================
  // Upload handler
  // =====================================================

  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault()

    if (!file || !countryId) {
      setStatus(
        "❌ Please select a country and CSV file."
      )
      return
    }

    setUploading(true)
    setStatus(null)

    try {
      const formData = new FormData()

      formData.append("file", file)

      formData.append(
        "country_id",
        String(countryId)
      )

      const response = await fetch(
        `${API_BASE}/api/trends/upload-csv`,
        {
          method: "POST",
          body: formData,
        }
      )

      if (!response.ok) {
        const text = await response.text()

        throw new Error(
          text || "Upload failed"
        )
      }

      const data = await response.json()

      console.log(
        "✅ Upload success:",
        data
      )

      setStatus(
        `✅ Uploaded ${data.rows_inserted} rows (${data.keywords_processed} keywords)`
      )

      // -------------------------------------------------
      // Run downstream analytics
      // -------------------------------------------------

      await runAnalysis()

      // reset form
      setFile(null)
      setCountryId(null)

      // reload uploads
      await loadUploads()

      // refresh dashboard
      navigate(
        `/dashboard?refresh=${Date.now()}`
      )

    } catch (err) {

      console.error(
        "❌ Upload error:",
        err
      )

      setStatus(
        err instanceof Error
          ? `❌ ${err.message}`
          : "❌ Upload failed"
      )

    } finally {

      setUploading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-8 space-y-12">

      {/* ================================================= */}
      {/* Upload Form */}
      {/* ================================================= */}

      <form onSubmit={handleSubmit}>

        <h1 className="text-2xl font-semibold mb-6">
          Upload Google Trends Data
        </h1>

        <div className="bg-white p-6 rounded shadow space-y-5">

          {/* Country selector */}

          <select
            className="w-full border rounded px-3 py-2"
            value={countryId ?? ""}
            disabled={loadingCountries}
            onChange={(e) =>
              setCountryId(
                Number(e.target.value)
              )
            }
          >

            <option value="">
              {loadingCountries
                ? "Loading countries..."
                : "Select country"}
            </option>

            {countries.map((country) => (
              <option
                key={country.id}
                value={country.id}
              >
                {country.name} (
                {country.iso2})
              </option>
            ))}

          </select>

          {/* File */}

          <input
            type="file"
            accept=".csv"
            className="w-full"
            onChange={(e) =>
              setFile(
                e.target.files?.[0] ?? null
              )
            }
          />

          {/* Submit */}

          <button
            type="submit"
            disabled={uploading}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-60"
          >
            {uploading
              ? "Uploading…"
              : "Upload & Analyze"}
          </button>

          {/* Status */}

          {status && (
            <p className="text-sm">
              {status}
            </p>
          )}

        </div>
      </form>

      {/* ================================================= */}
      {/* Upload History */}
      {/* ================================================= */}

      <div>

        <h2 className="text-xl font-semibold mb-4">
          Upload History
        </h2>

        {loadingTable ? (

          <p>Loading uploads…</p>

        ) : uploads.length === 0 ? (

          <p className="text-gray-500">
            No uploads yet.
          </p>

        ) : (

          <table className="w-full border">

            <thead className="bg-gray-100">

              <tr>

                <th className="p-2 border">
                  Keywords
                </th>

                <th className="p-2 border">
                  Country
                </th>

                <th className="p-2 border">
                  Rows
                </th>

                <th className="p-2 border">
                  Uploaded
                </th>

              </tr>

            </thead>

            <tbody>

              {uploads.map((u) => (

                <tr
                  key={u.id}
                  className="cursor-pointer hover:bg-indigo-50"
                  onClick={() =>
                    navigate(
                      `/dashboard?refresh=${Date.now()}`
                    )
                  }
                >

                  {/* Keywords */}

                  <td className="p-2 border">
                    {u.keyword}
                  </td>

                  {/* Country */}

                  <td className="p-2 border">
                    {u.country.name} (
                    {u.country.iso2})
                  </td>

                  {/* Rows */}

                  <td className="p-2 border text-center">
                    {u.rows_inserted}
                  </td>

                  {/* Uploaded */}

                  <td className="p-2 border">
                    {new Date(
                      u.uploaded_at
                    ).toLocaleString()}
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