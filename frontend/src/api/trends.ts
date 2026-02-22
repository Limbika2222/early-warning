// src/api/trends.ts

// --------------------------------
// Shared types
// --------------------------------
export type TrendPoint = {
  date: string
  value: number
}

export type UploadHistoryItem = {
  id: number
  keyword: string
  disease_id: number
  country: string
  rows_inserted: number
  uploaded_at: string
}

// Base path (relies on Vite proxy or same-origin deployment)
const API_BASE = `${import.meta.env.VITE_API_BASE}/api/trends`

// --------------------------------
// Helper: Safe fetch wrapper
// --------------------------------
async function safeFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options)

  const contentType = res.headers.get("content-type")

  if (!res.ok) {
    if (contentType?.includes("application/json")) {
      const errorData = await res.json()
      throw new Error(errorData.detail || "Request failed")
    } else {
      const text = await res.text()
      throw new Error(text || "Request failed")
    }
  }

  return res.json()
}

// --------------------------------
// Interest over time (single keyword)
// --------------------------------
export async function fetchInterestOverTime(
  keywordId: number,
  countryId: number
): Promise<TrendPoint[]> {
  return safeFetch<TrendPoint[]>(
    `${API_BASE}/interest-over-time?keyword_id=${keywordId}&country_id=${countryId}`
  )
}

// --------------------------------
// Aggregated disease signal
// Supports optional date range
// --------------------------------
export async function fetchAggregatedDiseaseSignal(
  diseaseId: number,
  countryId: number,
  startDate?: string,
  endDate?: string
): Promise<TrendPoint[]> {

  const params = new URLSearchParams()
  params.set("disease_id", String(diseaseId))
  params.set("country_id", String(countryId))

  if (startDate) params.set("start_date", startDate)
  if (endDate) params.set("end_date", endDate)

  return safeFetch<TrendPoint[]>(
    `${API_BASE}/aggregate?${params.toString()}`
  )
}

// --------------------------------
// Upload CSV
// --------------------------------
export async function uploadCsv(
  formData: FormData
): Promise<{
  status: string
  rows_inserted: number
  date_range: { start: string; end: string }
}> {
  return safeFetch(
    `${API_BASE}/upload-csv`,
    {
      method: "POST",
      body: formData,
    }
  )
}

// --------------------------------
// Upload history
// --------------------------------
export async function fetchUploadHistory(): Promise<UploadHistoryItem[]> {
  return safeFetch<UploadHistoryItem[]>(
    `${API_BASE}/uploads`
  )
}