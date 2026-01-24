// src/api/trends.ts

export type TrendPoint = {
  date: string
  value: number
}

export type UploadedDataset = {
  keyword: string
  country: string
  start_date: string
  end_date: string
  row_count: number
  upload_date: string
}

const API_BASE = "/api/trends"

// -----------------------------
// Existing function
// -----------------------------
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

// -----------------------------
// Fetch uploaded datasets
// -----------------------------
export type DatasetQueryParams = {
  search?: string
  sort_by?: "keyword" | "country" | "upload_date"
  order?: "asc" | "desc"
}

export async function fetchUploadedDatasets(
  params: DatasetQueryParams = {}
): Promise<UploadedDataset[]> {
  const query = new URLSearchParams()

  if (params.search) query.set("search", params.search)
  if (params.sort_by) query.set("sort_by", params.sort_by)
  if (params.order) query.set("order", params.order)

  const res = await fetch(`${API_BASE}/datasets?${query.toString()}`)

  if (!res.ok) {
    throw new Error("Failed to fetch uploaded datasets")
  }

  return res.json()
}
