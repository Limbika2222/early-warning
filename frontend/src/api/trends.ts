// src/api/trends.ts

// --------------------------------
// Types
// --------------------------------
export type TrendPoint = {
  date: string
  value: number
}

export type UploadHistoryItem = {
  id: number
  keyword: string        // 🔥 matches backend (keywords string)
  country: string
  rows_inserted: number
  uploaded_at: string
}

// --------------------------------
// Environment validation
// --------------------------------
const RAW_BASE = import.meta.env.VITE_API_BASE

if (!RAW_BASE) {
  throw new Error(
    "VITE_API_BASE is not defined. Check your frontend/.env file."
  )
}

// Remove trailing slash
const CLEAN_BASE = RAW_BASE.endsWith("/")
  ? RAW_BASE.slice(0, -1)
  : RAW_BASE

// Final API base
const API_BASE = `${CLEAN_BASE}/api/trends`

// --------------------------------
// Helper: Safe fetch
// --------------------------------
async function safeFetch<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  try {
    const res = await fetch(url, options)

    const contentType = res.headers.get("content-type")

    if (!res.ok) {
      if (contentType?.includes("application/json")) {
        const errorData = await res.json()
        console.error("❌ API Error:", errorData)
        throw new Error(errorData.detail || "Request failed")
      } else {
        const text = await res.text()
        console.error("❌ API Error:", text)
        throw new Error(text || "Request failed")
      }
    }

    return res.json()
  } catch (err) {
    console.error("❌ Fetch failed:", err)
    throw err
  }
}

// --------------------------------
// Interest over time
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
// Upload CSV (🔥 FIXED TYPE)
// --------------------------------
export async function uploadCsv(
  formData: FormData
): Promise<{
  status: string
  upload_id: number
  keywords_processed: number
  rows_inserted: number
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
// Upload history (🔥 MATCHES BACKEND)
// --------------------------------
export async function fetchUploadHistory(): Promise<UploadHistoryItem[]> {
  return safeFetch<UploadHistoryItem[]>(
    `${API_BASE}/uploads`
  )
}