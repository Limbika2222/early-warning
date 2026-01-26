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
  country: string
  rows_inserted: number
  uploaded_at: string
}

const API_BASE = "/api/trends"

// --------------------------------
// Interest over time (single keyword)
// --------------------------------
export async function fetchInterestOverTime(
  keywordId: number,
  countryId: number
): Promise<TrendPoint[]> {
  const res = await fetch(
    `${API_BASE}/interest-over-time?keyword_id=${keywordId}&country_id=${countryId}`
  )

  if (!res.ok) {
    throw new Error("Failed to fetch Google Trends data")
  }

  return res.json()
}

// --------------------------------
// Aggregated disease signal
// Supports optional date range ✅
// --------------------------------
export async function fetchAggregatedDiseaseSignal(
  diseaseId: number,
  countryId: number,
  startDate?: string, // YYYY-MM-DD
  endDate?: string    // YYYY-MM-DD
): Promise<TrendPoint[]> {
  const params = new URLSearchParams()

  params.set("disease_id", String(diseaseId))
  params.set("country_id", String(countryId))

  if (startDate) {
    params.set("start_date", startDate)
  }

  if (endDate) {
    params.set("end_date", endDate)
  }

  const res = await fetch(`${API_BASE}/aggregate?${params.toString()}`)

  if (!res.ok) {
    throw new Error("Failed to fetch aggregated disease signal")
  }

  return res.json()
}

// --------------------------------
// Upload history (OPTION B – every upload)
// --------------------------------
export async function fetchUploadHistory(): Promise<UploadHistoryItem[]> {
  const res = await fetch(`${API_BASE}/uploads`)

  if (!res.ok) {
    throw new Error("Failed to fetch upload history")
  }

  return res.json()
}
